# accounts/views.py

import datetime
import json

from django import forms
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Count, OuterRef, Q, Subquery
from django.forms import modelformset_factory
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from training.forms import BodyMetricEntryForm, WorkoutSessionForm
from training.models import (
    BodyMetricEntry,
    ClientProgramme,
    ConsultationRequest,
    ContactQuery,
    ProgrammeBlock,
    ProgrammeDay,
    ProgrammeExercise,
    SupportMessage,
    SupportTicket,
    WorkoutSession,
)

from .models import ClientProfile
from .services.consultation_assignment import assign_consultation_to_trainer


def is_trainer(user):
    """
    For now we'll treat Django's is_staff flag as 'trainer / owner'.

    Later we can upgrade this to Groups or custom roles
    without changing the rest of the code.
    """
    return user.is_staff


def staff_required(view_func):
    # Must be defined before decorators are evaluated.
    return user_passes_test(
        lambda u: u.is_staff,
        login_url="accounts:trainer_login",
    )(view_func)


User = get_user_model()


class TrainerWorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ["notes"]


class TrainerLoginView(LoginView):
    """
    Trainer / owner login using Django's built-in authentication.
    """

    template_name = "accounts/trainer_login.html"

    def get_success_url(self):
        # Superusers (owners) land on the owner dashboard;
        # trainers go to theirs.
        if self.request.user.is_superuser:
            return reverse_lazy("accounts:owner_dashboard")
        return reverse_lazy("accounts:trainer_dashboard")


class ClientLoginView(LoginView):
    """
    Client login using Django's built-in authentication.
    """

    template_name = "accounts/client_login.html"

    def get_success_url(self):
        return reverse_lazy("accounts:client_dashboard")


@login_required
def client_dashboard(request):
    """
    Dashboard for coaching clients.

    Shows basic information from the linked ClientProfile and will later
    surface programme, log, and metrics data.
    """
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    profile = None
    try:
        profile = request.user.client_profile
    except ClientProfile.DoesNotExist:
        pass

    active_assignment = (
        ClientProgramme.objects.filter(
            client=request.user,
            status="active",
        )
        .select_related("block")
        .order_by("-start_date", "-id")
        .first()
    )

    plan = None
    completed = False

    if active_assignment and active_assignment.block:
        block = active_assignment.block
        days = list(block.days.all().order_by("order"))

        if days:
            last_session = (
                WorkoutSession.objects.filter(
                    client=request.user,
                    client_programme=active_assignment,
                )
                .select_related("programme_day")
                .order_by(
                    "-week_number",
                    "-programme_day__order",
                    "-date",
                    "-id",
                )
                .first()
            )

            next_week = 1
            next_day = days[0]

            if last_session and last_session.programme_day:
                current_day_order = last_session.programme_day.order or 0
                next_week = last_session.week_number or 1

                later_day = next(
                    (
                        d
                        for d in days
                        if (d.order or 0) > current_day_order
                    ),
                    None,
                )

                if later_day:
                    next_day = later_day
                else:
                    if next_week < block.weeks:
                        next_week += 1
                        next_day = days[0]
                    else:
                        completed = True

            if not completed:
                start_url = reverse_lazy(
                    "accounts:client_programme_library"
                )
                start_url = f"{start_url}?week={next_week}#day-{next_day.id}"

                clean_name = next_day.name or ""
                if clean_name.lower().startswith("day "):
                    parts = clean_name.split("-", 1)
                    if len(parts) == 2:
                        clean_name = parts[1].strip()

                plan = {
                    "week": next_week,
                    "day": next_day,
                    "day_number": next_day.order or 1,
                    "exercise_count": next_day.exercises.count(),
                    "start_url": start_url,
                    "day_display": clean_name,
                }

    context = {
        "profile": profile,
        "latest_sessions": [],
        "latest_metrics": [],
        "plan": plan,
        "assignment": active_assignment,
        "completed": completed,
        "stats": {},
    }

    since_date = timezone.localdate() - datetime.timedelta(days=7)
    prev_start = since_date - datetime.timedelta(days=7)

    sessions_completed = WorkoutSession.objects.filter(
        client=request.user,
        date__gte=since_date,
    ).count()
    sessions_prev = WorkoutSession.objects.filter(
        client=request.user,
        date__gte=prev_start,
        date__lt=since_date,
    ).count()

    metrics_qs = BodyMetricEntry.objects.filter(
        client=request.user,
        date__gte=since_date,
    )
    sleep_avg = metrics_qs.aggregate(avg=Avg("sleep_hours")).get("avg")
    sleep_prev = (
        BodyMetricEntry.objects.filter(
            client=request.user,
            date__gte=prev_start,
            date__lt=since_date,
        ).aggregate(avg=Avg("sleep_hours")).get("avg")
    )

    latest_metric = (
        BodyMetricEntry.objects.filter(client=request.user)
        .order_by("-date", "-created_at")
        .first()
    )

    latest_bodyweight = (
        latest_metric.bodyweight_kg if latest_metric else None
    )
    latest_bench = (
        latest_metric.bench_top_set_kg if latest_metric else None
    )

    prev_metric = (
        BodyMetricEntry.objects.filter(
            client=request.user,
            date__gte=prev_start,
            date__lt=since_date,
        )
        .order_by("-date", "-created_at")
        .first()
    )
    prev_bodyweight = (
        prev_metric.bodyweight_kg if prev_metric else None
    )
    prev_bench = prev_metric.bench_top_set_kg if prev_metric else None

    def format_delta(delta, is_float=False, suffix=""):
        if delta is None:
            return "No comparison", "na"
        if abs(delta) < 1e-9:
            return "No change", "neutral"
        direction = "Up" if delta > 0 else "Down"
        magnitude = abs(delta)
        if is_float:
            mag_str = f"{magnitude:.1f}"
        else:
            mag_str = f"{int(magnitude)}"
        return f"{direction} {mag_str}{suffix}", (
            "up" if delta > 0 else "down"
        )

    sessions_delta_text, sessions_delta_class = format_delta(
        sessions_completed - sessions_prev,
        is_float=False,
    )

    sleep_delta = None
    if sleep_avg is not None and sleep_prev is not None:
        sleep_delta = sleep_avg - sleep_prev
    sleep_delta_text, sleep_delta_class = format_delta(
        sleep_delta,
        is_float=True,
        suffix=" h",
    )

    bw_delta = None
    if latest_bodyweight is not None and prev_bodyweight is not None:
        bw_delta = latest_bodyweight - prev_bodyweight
    bw_delta_text, bw_delta_class = format_delta(
        bw_delta,
        is_float=True,
        suffix=" kg",
    )

    bench_delta = None
    if latest_bench is not None and prev_bench is not None:
        bench_delta = latest_bench - prev_bench
    bench_delta_text, bench_delta_class = format_delta(
        bench_delta,
        is_float=True,
        suffix=" kg",
    )

    context["stats"] = {
        "sessions": {
            "value": sessions_completed,
            "delta_text": sessions_delta_text,
            "delta_class": sessions_delta_class,
            "hint": "Last 7 days",
        },
        "sleep": {
            "value": sleep_avg,
            "delta_text": sleep_delta_text,
            "delta_class": sleep_delta_class,
            "hint": "Last 7 days",
        },
        "bodyweight": {
            "value": latest_bodyweight,
            "delta_text": bw_delta_text,
            "delta_class": bw_delta_class,
            "hint": "Most recent entry",
        },
        "bench": {
            "value": latest_bench,
            "delta_text": bench_delta_text,
            "delta_class": bench_delta_class,
            "hint": "Most recent entry",
        },
    }
    return render(request, "client/dashboard.html", context)


@login_required
def client_today(request):
    """Display the current day's training plan for the logged-in client."""
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    active_assignment = (
        ClientProgramme.objects.filter(
            client=request.user,
            status="active",
        )
        .select_related("block")
        .order_by("-start_date", "-id")
        .first()
    )

    if not active_assignment or not active_assignment.block:
        return render(
            request,
            "client/today.html",
            {"plan": None, "assignment": None},
        )

    block = active_assignment.block
    days = list(block.days.all().order_by("order"))

    if not days:
        return render(
            request,
            "client/today.html",
            {"plan": None, "assignment": active_assignment},
        )

    last_session = (
        WorkoutSession.objects.filter(
            client=request.user,
            client_programme=active_assignment,
        )
        .select_related("programme_day")
        .order_by("-week_number", "-programme_day__order", "-date", "-id")
        .first()
    )

    next_week = 1
    next_day = days[0]
    completed = False

    if last_session and last_session.programme_day:
        current_day_order = last_session.programme_day.order or 0
        next_week = last_session.week_number or 1

        later_day = next(
            (
                d
                for d in days
                if (d.order or 0) > current_day_order
            ),
            None,
        )

        if later_day:
            next_day = later_day
        else:
            if next_week < block.weeks:
                next_week += 1
                next_day = days[0]
            else:
                completed = True

    if completed:
        return render(
            request,
            "client/today.html",
            {
                "plan": None,
                "assignment": active_assignment,
                "completed": True,
            },
        )

    start_url = reverse_lazy("accounts:client_programme_library")
    start_url = f"{start_url}?week={next_week}#day-{next_day.id}"

    clean_name = next_day.name or ""
    if clean_name.lower().startswith("day "):
        parts = clean_name.split("-", 1)
        if len(parts) == 2:
            clean_name = parts[1].strip()

    plan = {
        "week": next_week,
        "day": next_day,
        "day_number": next_day.order or 1,
        "exercise_count": next_day.exercises.count(),
        "start_url": start_url,
        "day_display": clean_name,
    }

    return render(
        request,
        "client/today.html",
        {
            "plan": plan,
            "assignment": active_assignment,
            "completed": False,
        },
    )


@login_required
def client_programme_library(request):
    """
    Show active programme assignments for the logged-in client,
    including blocks, days, and exercises.
    """
    assignments = (
        ClientProgramme.objects.filter(client=request.user, status="active")
        .select_related("block", "trainer")
        .prefetch_related("block__days__exercises")
        .order_by("start_date", "block__name")
    )

    context = {"assignments": assignments}
    return render(request, "client/programme_library.html", context)


@login_required
def client_workout_log(request):
    """
    Client workout log page.

    - Direct entry defaults to the first available ProgrammeDay.
    - Loads real ProgrammeExercise rows for the selected day.
    - Saves via WorkoutSessionForm and compiles per-exercise inputs
      into notes.
    - Redirects back with ?day=<id> so the same exercises render after save.
    """
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    initial = {}
    session_name_param = (request.GET.get("session_name") or "").strip()
    selected_week_param = request.GET.get("week") or request.POST.get("week")
    selected_week = 1

    active_assignments = (
        ClientProgramme.objects.filter(client=request.user, status="active")
        .select_related("block")
        .order_by("start_date", "block__name")
    )

    available_days_qs = (
        ProgrammeDay.objects.filter(
            block__in=active_assignments.values_list("block_id", flat=True)
        )
        .select_related("block")
        .order_by("block__name", "order")
    )

    day_id = request.GET.get("day") or request.POST.get("day")
    programme_day = None

    if day_id and day_id.isdigit():
        programme_day = available_days_qs.filter(id=int(day_id)).first()

    if programme_day is None and session_name_param:
        programme_day = available_days_qs.filter(
            name=session_name_param
        ).first()

    if programme_day is None:
        programme_day = available_days_qs.first()

    if programme_day:
        programme_exercises = list(
            programme_day.exercises.all().order_by("order")
        )
        initial["name"] = programme_day.name
    else:
        programme_exercises = []

    if programme_day and selected_week_param and selected_week_param.isdigit():
        selected_week = int(selected_week_param)
    max_weeks = 6
    if programme_day and programme_day.block:
        max_weeks = programme_day.block.weeks
    if selected_week < 1:
        selected_week = 1
    if selected_week > max_weeks:
        selected_week = max_weeks
    week_options = list(range(1, max_weeks + 1))

    session_qs = (
        WorkoutSession.objects.filter(client=request.user)
        .order_by("-date", "-created_at")
    )
    paginator = Paginator(session_qs, 5)
    page_number = request.GET.get("page")
    recent_sessions = paginator.get_page(page_number)

    # Keep filters when paging (currently no extra filters on sessions list).
    sessions_qs = request.GET.copy()
    sessions_qs.pop("page", None)
    sessions_base_qs = sessions_qs.urlencode()
    sessions_base_qs = f"&{sessions_base_qs}" if sessions_base_qs else ""

    if request.method == "POST":
        post_data = request.POST.copy()

        if programme_day:
            post_data["name"] = programme_day.name

        form = WorkoutSessionForm(post_data)

        if form.is_valid():
            cd = form.cleaned_data
            base_notes = (cd.get("notes") or "").strip()
            client_programme = None
            if programme_day:
                client_programme = active_assignments.filter(
                    block=programme_day.block
                ).first()

            detail_lines = []
            if programme_day and programme_exercises:
                detail_lines.append("Session details:")

                for ex in programme_exercises:
                    set1 = (request.POST.get(f"ex_{ex.id}_set1") or "-")
                    set2 = (request.POST.get(f"ex_{ex.id}_set2") or "-")
                    set3 = (request.POST.get(f"ex_{ex.id}_set3") or "-")
                    weight_val = request.POST.get(f"ex_{ex.id}_weight") or "-"

                    set1 = set1.strip()
                    set2 = set2.strip()
                    set3 = set3.strip()
                    weight_val = weight_val.strip()

                    target_weight = ex.target_weight_kg or "-"
                    header = (
                        f"{ex.exercise_name} "
                        f"({ex.target_sets} x {ex.target_reps} "
                        f"@ {target_weight})"
                    )
                    results = (
                        f"{set1} | {set2} | {set3} "
                        f"(weight: {weight_val})"
                    )
                    detail_lines.append(f"{header}: {results}")

            compiled_details = "\n".join(detail_lines).strip()

            if base_notes and compiled_details:
                session_notes = f"{base_notes}\n\n{compiled_details}"
            elif compiled_details:
                session_notes = compiled_details
            else:
                session_notes = base_notes

            existing_session = None
            if programme_day and client_programme:
                existing_session = WorkoutSession.objects.filter(
                    client=request.user,
                    client_programme=client_programme,
                    programme_day=programme_day,
                    week_number=selected_week,
                ).first()

            if existing_session:
                messages.error(
                    request,
                    (
                        "This session log already exist for "
                        f"Week {selected_week}/{programme_day.name}. "
                        "Please edit session below if needed."
                    ),
                )
                redirect_url = reverse_lazy("accounts:client_workout_log")
                params = [f"day={programme_day.id}", f"week={selected_week}"]
                redirect_url = f"{redirect_url}?{'&'.join(params)}"
                return redirect(redirect_url)

            session = form.save(commit=False)

            if not session.date:
                session.date = timezone.localdate()

            if getattr(session, "client_id", None) is None:
                session.client = request.user

            session.client_programme = client_programme
            session.programme_day = programme_day
            session.week_number = selected_week
            if programme_day:
                session.name = f"Week {selected_week} - {programme_day.name}"
            session.notes = session_notes
            session.save()

            messages.success(request, "Workout session saved.")

            redirect_url = reverse_lazy("accounts:client_workout_log")
            query_bits = []
            if programme_day:
                query_bits.append(f"day={programme_day.id}")
            if selected_week:
                query_bits.append(f"week={selected_week}")
            if query_bits:
                redirect_url = f"{redirect_url}?{'&'.join(query_bits)}"
            return redirect(redirect_url)
    else:
        form = WorkoutSessionForm(initial=initial)

    context = {
        "sessions": recent_sessions,
        "sessions_base_qs": sessions_base_qs,
        "session_form": form,
        "programme_day": programme_day,
        "programme_exercises": programme_exercises,
        "available_days": list(available_days_qs),
        "week_options": week_options,
        "selected_week": selected_week,
    }
    return render(request, "client/workout_log.html", context)


@login_required
def client_workout_edit(request):
    """
    Handle edits to an existing workout session from the client modal.
    Only updates sessions belonging to the logged-in user.
    """
    if request.method != "POST":
        return redirect("accounts:client_workout_log")

    session_id = request.POST.get("session_id")
    if not session_id:
        messages.error(request, "Missing workout session id.")
        return redirect("accounts:client_workout_log")

    session = get_object_or_404(
        WorkoutSession,
        pk=session_id,
        client=request.user,
    )

    name_val = (request.POST.get("name") or "").strip()
    notes_val = request.POST.get("notes")
    status_val = (request.POST.get("status") or "").strip()

    if name_val:
        session.name = name_val

    if notes_val is not None:
        session.notes = notes_val

    if status_val and hasattr(session, "status"):
        session.status = status_val

    session.save()
    messages.success(request, "Workout session updated.")
    return redirect("accounts:client_workout_log")


@login_required
def client_metrics(request):
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    user = request.user

    action = request.POST.get("action", "").strip().lower()

    if request.method == "POST" and action in {"update", "delete"}:
        entry_id = request.POST.get("entry_id")
        entry = get_object_or_404(BodyMetricEntry, id=entry_id, client=user)

        if action == "delete":
            entry.delete()
            messages.success(request, "Check-in deleted.")
            return redirect("accounts:client_metrics")

        form = BodyMetricEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Check-in updated.")
            return redirect("accounts:client_metrics")
    elif request.method == "POST":
        form = BodyMetricEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.client = user
            entry.save()
            messages.success(request, "Body metrics check-in saved.")
            return redirect("accounts:client_metrics")
    else:
        form = BodyMetricEntryForm(initial={"date": timezone.localdate()})

    entries_qs = BodyMetricEntry.objects.filter(client=user).order_by(
        "date",
        "created_at",
    )
    entries = list(entries_qs)

    def latest_and_change(field_name):
        latest_entry = None
        for e in reversed(entries):
            value = getattr(e, field_name)
            if value is not None:
                latest_entry = e
                break

        if latest_entry is None:
            return None, None

        latest_value = getattr(latest_entry, field_name)
        latest_date = latest_entry.date
        cutoff = latest_date - datetime.timedelta(weeks=4)

        baseline_entry = None
        for e in entries:
            if e.date <= cutoff and getattr(e, field_name) is not None:
                baseline_entry = e

        if baseline_entry is None:
            change = None
        else:
            change = latest_value - getattr(baseline_entry, field_name)

        return latest_value, change

    summary_rows = []
    metrics_spec = [
        {
            "label": "Bodyweight",
            "field": "bodyweight_kg",
            "unit": "kg",
            "target_display": "77.5 kg",
        },
        {
            "label": "Waist",
            "field": "waist_cm",
            "unit": "cm",
            "target_display": "82 cm",
        },
        {
            "label": "Bench top set",
            "field": "bench_top_set_kg",
            "unit": "kg",
            "target_display": "62.5 kg x 8",
        },
        {
            "label": "Sleep average",
            "field": "sleep_hours",
            "unit": "h",
            "target_display": "7.5 h",
        },
    ]

    for spec in metrics_spec:
        latest, change = latest_and_change(spec["field"])
        summary_rows.append(
            {
                "label": spec["label"],
                "unit": spec["unit"],
                "target_display": spec["target_display"],
                "latest": latest,
                "change": change,
            }
        )

    recent_entries = BodyMetricEntry.objects.filter(client=user).order_by(
        "-date",
        "-created_at",
    )[:5]

    chart_entries = BodyMetricEntry.objects.filter(
        client=user
    ).order_by("date")
    chart_labels = [entry.date.strftime("%d %b") for entry in chart_entries]

    bodyweight_series = [
        float(entry.bodyweight_kg) if entry.bodyweight_kg is not None else None
        for entry in chart_entries
    ]
    bench_series = [
        float(entry.bench_top_set_kg)
        if entry.bench_top_set_kg is not None
        else None
        for entry in chart_entries
    ]

    has_bodyweight_data = any(v is not None for v in bodyweight_series)
    has_bench_data = any(v is not None for v in bench_series)

    context = {
        "form": form,
        "summary_rows": summary_rows,
        "recent_entries": recent_entries,
        "chart_labels_json": json.dumps(chart_labels),
        "bodyweight_series_json": json.dumps(bodyweight_series),
        "bench_series_json": json.dumps(bench_series),
        "has_bodyweight_data": has_bodyweight_data,
        "has_bench_data": has_bench_data,
    }
    return render(request, "client/metrics.html", context)


@login_required
def client_support(request):
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    tickets = SupportTicket.objects.filter(
        client=request.user,
    ).order_by("-updated_at", "-created_at")

    if request.method == "POST":
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if subject and message:
            trainer = None
            profile = ClientProfile.objects.filter(user=request.user).first()
            if profile:
                trainer = profile.preferred_trainer

            ticket = SupportTicket.objects.create(
                client=request.user,
                trainer=trainer,
                subject=subject,
                status=SupportTicket.STATUS_OPEN,
            )
            SupportMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                body=message,
            )

            success_text = (
                "Support request sent to your coach."
                if trainer
                else "Support request sent."
            )
            messages.success(
                request,
                success_text,
            )
            return redirect("accounts:client_support")

        messages.error(request, "Both subject and message are required.")

    return render(
        request,
        "client/support.html",
        {"tickets": tickets},
    )


@login_required
def client_support_tickets(request):
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    tickets = SupportTicket.objects.filter(
        client=request.user,
    ).order_by("-updated_at", "-created_at")

    return render(
        request,
        "client/support_tickets.html",
        {"tickets": tickets},
    )


@login_required
def client_support_ticket_detail(request, ticket_id):
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    ticket = get_object_or_404(
        SupportTicket,
        id=ticket_id,
        client=request.user,
    )

    thread = SupportMessage.objects.filter(
        ticket=ticket,
    ).order_by("created_at")

    if request.method == "POST":
        action = request.POST.get("action", "").lower()

        if action == "close":
            ticket.status = SupportTicket.STATUS_CLOSED
            ticket.save(update_fields=["status", "updated_at"])
            messages.success(request, "Ticket closed.")
            return redirect(
                "accounts:client_support_ticket_detail",
                ticket_id=ticket.id,
            )

        body = request.POST.get("body", "").strip()
        if not body:
            messages.error(request, "Message cannot be empty.")
            return redirect(
                "accounts:client_support_ticket_detail",
                ticket_id=ticket.id,
            )

        SupportMessage.objects.create(
            ticket=ticket,
            sender=request.user,
            body=body,
        )
        ticket.status = SupportTicket.STATUS_WAITING
        ticket.save(update_fields=["status", "updated_at"])

        messages.success(request, "Reply sent.")
        return redirect(
            "accounts:client_support_ticket_detail",
            ticket_id=ticket.id,
        )

    return render(
        request,
        "client/support_ticket_detail.html",
        {
            "ticket": ticket,
            "thread": thread,
        },
    )


@login_required
def trainer_support(request):
    if not request.user.is_staff:
        return redirect("accounts:client_dashboard")

    # Use SupportTicket.trainer as the assignment link to enforce privacy.
    tickets_qs = SupportTicket.objects.filter(trainer=request.user)

    tickets = tickets_qs.order_by("-updated_at", "-created_at")
    status_counts = {
        "open": tickets_qs.filter(status=SupportTicket.STATUS_OPEN).count(),
        "waiting": tickets_qs.filter(
            status=SupportTicket.STATUS_WAITING
        ).count(),
        "closed": tickets_qs.filter(
            status=SupportTicket.STATUS_CLOSED
        ).count(),
    }

    # Owners see owner-branded template; trainers see trainer template.
    template = (
        "owner/support_inbox.html"
        if request.user.is_superuser
        else "trainer/support_inbox.html"
    )

    return render(
        request,
        template,
        {
            "tickets": tickets,
            "status_counts": status_counts,
            "current": "trainer_support",
        },
    )


@login_required
def trainer_support_ticket(request, ticket_id):
    if not request.user.is_staff:
        return redirect("accounts:client_dashboard")

    # Same privacy rule: only the assigned trainer (owner counts as trainer)
    # can view a ticket; others get 404 to avoid leaking existence.
    ticket = get_object_or_404(
        SupportTicket,
        id=ticket_id,
        trainer=request.user,
    )

    thread = SupportMessage.objects.filter(ticket=ticket).order_by("created_at")

    if request.method == "POST":
        action = request.POST.get("action", "").lower()
        body = request.POST.get("body", "").strip()

        if action == "reply":
            if not body:
                messages.error(request, "Message cannot be empty.")
                return redirect(
                    "accounts:trainer_support_ticket",
                    ticket_id=ticket.id,
                )

            SupportMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                body=body,
            )
            ticket.status = SupportTicket.STATUS_WAITING
            ticket.save(update_fields=["status", "updated_at"])
            messages.success(request, "Reply sent.")

        elif action == "close":
            ticket.status = SupportTicket.STATUS_CLOSED
            ticket.save(update_fields=["status", "updated_at"])
            messages.success(request, "Ticket closed.")

        elif action == "reopen":
            ticket.status = SupportTicket.STATUS_OPEN
            ticket.save(update_fields=["status", "updated_at"])
            messages.success(request, "Ticket reopened.")

        return redirect(
            "accounts:trainer_support_ticket",
            ticket_id=ticket.id,
        )

    return render(
        request,
        (
            "owner/support_ticket_detail.html"
            if request.user.is_superuser
            else "trainer/support_ticket_detail.html"
        ),
        {
            "ticket": ticket,
            "thread": thread,
            "current": "trainer_support",
        },
    )


@login_required(login_url="accounts:trainer_login")
@staff_required
def owner_dashboard(request):
    """
    Owner dashboard:
    - Only superusers can access; other staff are redirected to the
      trainer dashboard.
    """
    if not request.user.is_superuser:
        return redirect("accounts:trainer_dashboard")

    return render(
        request,
        "owner/dashboard.html",
        {"current": "owner_dashboard"},
    )


def owner_queries(request):
    """
    Owner-only list of incoming contact queries.
    Shows newest first with optional status filter.
    """
    if not request.user.is_superuser:
        return redirect("accounts:trainer_dashboard")

    selected_status = request.GET.get("status", "new")
    queries = ContactQuery.objects.all().order_by("-created_at")

    if selected_status and selected_status != "all":
        queries = queries.filter(status=selected_status)

    # Queries specifically assigned to the current owner for quick access.
    my_queries = ContactQuery.objects.filter(
        assigned_trainer=request.user
    ).order_by("-created_at")

    # Build base querystrings for each paginator (exclude page params).
    qs_params = request.GET.copy()
    qs_params.pop("inbox_page", None)
    qs_params.pop("my_page", None)
    inbox_base = qs_params.urlencode()
    inbox_base = f"&{inbox_base}" if inbox_base else ""

    my_qs_params = request.GET.copy()
    my_qs_params.pop("my_page", None)
    my_qs_params.pop("inbox_page", None)
    my_base = my_qs_params.urlencode()
    my_base = f"&{my_base}" if my_base else ""

    # Paginate inbox and my-queries independently to avoid param clashes.
    inbox_page_number = request.GET.get("inbox_page")
    my_page_number = request.GET.get("my_page")

    # Show 5 queries per page to keep lists compact.
    inbox_paginator = Paginator(queries, 5)
    my_paginator = Paginator(my_queries, 5)

    inbox_page_obj = inbox_paginator.get_page(inbox_page_number)
    my_page_obj = my_paginator.get_page(my_page_number)

    context = {
        "inbox_page_obj": inbox_page_obj,
        "selected_status": selected_status,
        "total_count": ContactQuery.objects.count(),
        "my_page_obj": my_page_obj,
        "inbox_base_qs": inbox_base,
        "my_base_qs": my_base,
        "current": "owner_queries",
    }
    return render(request, "owner/queries_inbox.html", context)


def owner_query_detail(request, pk):
    """
    Owner-only detail page for a single contact query with assignment/status.
    """
    if not request.user.is_superuser:
        return redirect("accounts:trainer_dashboard")

    query = get_object_or_404(ContactQuery, pk=pk)

    # Build trainer list (staff users) so owners can assign queries.
    trainers = (
        User.objects.filter(is_staff=True)
        .exclude(pk=request.user.pk)
        .order_by("last_name", "first_name", "username")
    )
    # Exclude owner; the dropdown has a dedicated "Assign to me" option.

    # Default selection: assigned trainer if present, otherwise "me".
    selected_assign = (
        query.assigned_trainer.pk if query.assigned_trainer else "me"
    )

    if request.method == "POST":
        # Assign trainer: "me", user id, or blank to unassign.
        assign_value = request.POST.get("assign_trainer", "").strip()
        if assign_value == "me":
            query.assigned_trainer = request.user
        elif assign_value:
            # Only allow ids in the trainer list.
            trainer = trainers.filter(pk=assign_value).first()
            query.assigned_trainer = trainer
        else:
            query.assigned_trainer = None

        # Update status if provided and valid.
        new_status = request.POST.get("status", "").strip()
        valid_statuses = [choice[0] for choice in ContactQuery.STATUS_CHOICES]
        if new_status in valid_statuses:
            query.status = new_status

        query.save()
        messages.success(request, "Query updated.")
        return redirect("accounts:owner_query_detail", pk=pk)

    context = {
        "query": query,
        "trainers": trainers,
        "status_choices": ContactQuery.STATUS_CHOICES,
        "selected_assign": selected_assign,
        "current": "owner_queries",
    }
    return render(request, "owner/query_detail.html", context)


def trainer_queries(request):
    """
    Trainer-only list of contact queries assigned to them.
    """
    if not request.user.is_staff:
        return redirect("accounts:client_dashboard")

    selected_status = request.GET.get("status", "all")
    queries = ContactQuery.objects.filter(
        assigned_trainer=request.user
    ).order_by("-created_at")

    if selected_status and selected_status != "all":
        queries = queries.filter(status=selected_status)

    # Paginate trainer inbox (5 per page).
    page_number = request.GET.get("page")
    paginator = Paginator(queries, 5)
    page_obj = paginator.get_page(page_number)

    # Base qs for pagination links (exclude page param).
    qs_params = request.GET.copy()
    qs_params.pop("page", None)
    base_qs = qs_params.urlencode()
    base_qs = f"&{base_qs}" if base_qs else ""

    context = {
        "page_obj": page_obj,
        "selected_status": selected_status,
        "base_qs": base_qs,
        "current": "trainer_queries",
    }
    return render(request, "trainer/queries_inbox.html", context)


def trainer_query_detail(request, pk):
    """
    Trainer-only view of a single query assigned to them.
    Trainers can update status but cannot reassign.
    """
    if not request.user.is_staff:
        return redirect("accounts:client_dashboard")

    query = get_object_or_404(
        ContactQuery,
        pk=pk,
        assigned_trainer=request.user,
    )

    if request.method == "POST":
        new_status = request.POST.get("status", "").strip()
        valid_statuses = [choice[0] for choice in ContactQuery.STATUS_CHOICES]
        if new_status in valid_statuses:
            query.status = new_status
            query.save()
            messages.success(request, "Query updated.")
        return redirect("accounts:trainer_query_detail", pk=pk)

    context = {
        "query": query,
        "status_choices": ContactQuery.STATUS_CHOICES,
        "current": "trainer_queries",
    }
    return render(request, "trainer/query_detail.html", context)


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_dashboard(request):
    """
    Trainer dashboard:
    - Shows latest consultation requests
    - Includes a small stats summary pulled from the database
    """
    status_filter = request.GET.get("status", "open")

    requests_qs = ConsultationRequest.objects.order_by("-created_at")
    if status_filter == "open":
        requests_qs = requests_qs.filter(
            status=ConsultationRequest.STATUS_NEW
        )
    elif status_filter == "dealt":
        requests_qs = requests_qs.filter(
            status__in=[
                ConsultationRequest.STATUS_ASSIGNED,
                ConsultationRequest.STATUS_ADDED_CLASSES,
            ]
        )
    paginator = Paginator(requests_qs, 5)
    page_number = request.GET.get("page")
    latest_requests = paginator.get_page(page_number)

    # Keep filters when paging consultation requests.
    req_params = request.GET.copy()
    req_params.pop("page", None)
    requests_base_qs = req_params.urlencode()
    requests_base_qs = f"&{requests_base_qs}" if requests_base_qs else ""
    total_requests = ConsultationRequest.objects.count()

    coaching_breakdown = (
        ConsultationRequest.objects.values("coaching_option")
        .annotate(count=Count("id"))
        .order_by("coaching_option")
    )

    choice_labels = dict(ConsultationRequest.COACHING_OPTION_CHOICES)
    for row in coaching_breakdown:
        row["label"] = choice_labels.get(
            row["coaching_option"],
            "Not specified",
        )

    classes_filter = request.GET.get("classes", "all")
    base_classes_qs = ConsultationRequest.objects.filter(
        status=ConsultationRequest.STATUS_ADDED_CLASSES,
        coaching_option__in=["small_group", "large_group"],
    ).order_by("-created_at")

    current_classes_qs = base_classes_qs
    if classes_filter == "small":
        current_classes_qs = current_classes_qs.filter(
            coaching_option="small_group"
        )
    elif classes_filter == "large":
        current_classes_qs = current_classes_qs.filter(
            coaching_option="large_group"
        )

    classes_paginator = Paginator(current_classes_qs, 5)
    classes_page_number = request.GET.get("classes_page")
    current_classes = classes_paginator.get_page(classes_page_number)

    # Keep filters when paging current classes.
    class_params = request.GET.copy()
    class_params.pop("classes_page", None)
    classes_base_qs = class_params.urlencode()
    classes_base_qs = f"&{classes_base_qs}" if classes_base_qs else ""

    total_classes_count = base_classes_qs.count()
    small_count = base_classes_qs.filter(
        coaching_option="small_group"
    ).count()
    large_count = base_classes_qs.filter(
        coaching_option="large_group"
    ).count()

    context = {
        "latest_requests": latest_requests,
        "total_requests": total_requests,
        "coaching_breakdown": coaching_breakdown,
        "status_filter": status_filter,
        "current_classes": current_classes,
        "classes_filter": classes_filter,
        "small_classes_count": small_count,
        "large_classes_count": large_count,
        "total_classes_count": total_classes_count,
        "requests_base_qs": requests_base_qs,
        "classes_base_qs": classes_base_qs,
    }
    # Owners see owner-branded template; trainers see trainer template.
    template = (
        "owner/dashboard.html"
        if request.user.is_superuser
        else "trainer/dashboard.html"
    )
    return render(request, template, context)


@login_required(login_url="accounts:trainer_login")
@staff_required
def add_to_current_classes(request, pk):
    """
    Mark a consultation as added to current classes
    (only for small/large group coaching options).
    """
    if request.method != "POST":
        return redirect("accounts:trainer_dashboard")

    consultation = get_object_or_404(ConsultationRequest, pk=pk)

    if consultation.coaching_option not in ["small_group", "large_group"]:
        messages.error(
            request,
            "Only group coaching requests can be added to classes.",
        )
        return redirect("accounts:trainer_consultation_detail", pk=pk)

    consultation.status = ConsultationRequest.STATUS_ADDED_CLASSES
    consultation.assigned_trainer = request.user
    consultation.save()
    messages.success(request, "Added to Current Classes.")
    return redirect("accounts:trainer_consultation_detail", pk=pk)


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_clients(request):
    """Show one row per email for the trainer's assigned clients."""
    trainer = request.user

    client_type = request.GET.get("type", "all")
    trainer_filter = request.GET.get("trainer", "all")

    # Annotate each consultation with a portal user id if an account exists.
    user_id_sq = User.objects.filter(
        email__iexact=OuterRef("email")
    ).values("id")[:1]

    if request.user.is_superuser:
        # Owners can view all trainers; start with all assigned clients.
        base_qs = ConsultationRequest.objects.filter(
            status=ConsultationRequest.STATUS_ASSIGNED,
            coaching_option__in=["1to1", "online"],
        )

        # Apply trainer filter before type filter.
        if trainer_filter == "me":
            base_qs = base_qs.filter(assigned_trainer=request.user)
        elif trainer_filter.isdigit():
            base_qs = base_qs.filter(assigned_trainer_id=int(trainer_filter))
        else:
            # "all" keeps the queryset untouched.
            pass
    else:
        base_qs = ConsultationRequest.objects.filter(
            assigned_trainer=trainer,
            status=ConsultationRequest.STATUS_ASSIGNED,
            coaching_option__in=["1to1", "online"],
        )

    base_qs = base_qs.annotate(
        portal_user_id=Subquery(user_id_sq)
    ).order_by("-created_at")

    if client_type == "online":
        qs = base_qs.filter(coaching_option="online")
    elif client_type == "1to1":
        qs = base_qs.filter(coaching_option="1to1")
    else:
        qs = base_qs

    # Paginate the filtered client list (5 per page).
    paginator = Paginator(qs, 5)
    page_number = request.GET.get("page")
    clients_page = paginator.get_page(page_number)

    # Build portal access links so trainers can share a working password-set URL
    # without relying on email delivery.
    portal_ids = [
        req.portal_user_id for req in clients_page if getattr(req, "portal_user_id", None)
    ]
    users_by_id = {u.id: u for u in User.objects.filter(id__in=portal_ids)}

    for req in clients_page:
        user = users_by_id.get(getattr(req, "portal_user_id", None))
        req.portal_user = user
        req.portal_link = None
        req.portal_username = None  # Clients log in using this username + their password.
        # Portal access == account exists and has a usable password set.
        req.portal_access = bool(user and user.has_usable_password())
        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            path = reverse_lazy(
                "password_reset_confirm",
                kwargs={"uidb64": uidb64, "token": token},
            )
            req.portal_link = request.build_absolute_uri(path)
            req.portal_username = user.username

    # Keep filters when paging clients list.
    client_params = request.GET.copy()
    client_params.pop("page", None)
    clients_base_qs = client_params.urlencode()
    clients_base_qs = f"&{clients_base_qs}" if clients_base_qs else ""

    # Owner already appears as "Me (...)", so exclude them to avoid duplicates.
    trainer_options = (
        User.objects.filter(is_active=True, is_staff=True)
        .exclude(id=request.user.id)
        .order_by("first_name", "last_name", "username")
    )

    context = {
        "trainer": trainer,
        "clients_page": clients_page,
        "client_type": client_type,
        "trainer_filter": trainer_filter,
        "trainer_options": trainer_options,
        "clients_base_qs": clients_base_qs,
        "section": "clients",
    }
    # Use owner template for superusers so branding stays consistent.
    template = (
        "owner/clients.html"
        if request.user.is_superuser
        else "trainer/clients.html"
    )
    return render(request, template, context)


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_metrics(request):
    """
    Trainer view: overview of latest body metric entries per client.
    """
    entries = BodyMetricEntry.objects.select_related("client").order_by(
        "client__id",
        "-date",
    )

    latest_by_user = {}
    for entry in entries:
        user_id = entry.client_id
        if user_id not in latest_by_user:
            latest_by_user[user_id] = entry

    client_rows = []
    for entry in latest_by_user.values():
        client = entry.client
        client_rows.append(
            {
                "client_name": client.get_full_name() or client.username,
                "email": client.email,
                "date": entry.date,
                "bodyweight": entry.bodyweight_kg,
                "waist": entry.waist_cm,
                "bench_topset": getattr(entry, "bench_top_set_kg", None),
            }
        )

    client_rows.sort(key=lambda row: row["client_name"].lower())

    # Owners see owner-branded template; trainers see trainer template.
    template = (
        "owner/metrics.html"
        if request.user.is_superuser
        else "trainer/metrics.html"
    )
    return render(
        request,
        template,
        {"client_rows": client_rows},
    )


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_programme_detail(request, block_id):
    """
    Trainer view: show a programme block with its days/exercises,
    allow assignment to a client (creates a tailored clone),
    and allow editing exercises ONLY for tailored copies (assigned blocks).
    """
    block = get_object_or_404(
        ProgrammeBlock.objects.prefetch_related(
            "days__exercises",
            "assignments",
        ),
        id=block_id,
    )

    is_template_block = block.is_template
    tailored_client = None
    assignable_clients = []
    assignment = None
    is_template_block = block.is_template

    template_block = block.parent_template if block.parent_template else block
    template_days_qs = (
        template_block.days.all()
        .order_by("order")
        .prefetch_related("exercises")
    )

    ExerciseFormSet = modelformset_factory(
        ProgrammeExercise,
        fields=("target_sets", "target_reps", "target_weight_kg"),
        extra=0,
    )

    def clone_programme_block(template_block_obj, trainer_user, client_user):
        """
        Deep clone ProgrammeBlock -> days -> exercises,
        so templates stay untouched.
        """
        cloned_block = ProgrammeBlock.objects.create(
            name=(
                f"{template_block_obj.name} "
                f"(Tailored for "
                f"{client_user.get_full_name() or client_user.username})"
            ),
            description=template_block_obj.description,
            weeks=template_block_obj.weeks,
            created_by=trainer_user,
            is_template=False,
            parent_template=template_block_obj,
        )

        for day in template_block_obj.days.all().order_by("order"):
            cloned_day = ProgrammeDay.objects.create(
                block=cloned_block,
                name=day.name,
                order=day.order,
            )

            for ex in day.exercises.all().order_by("order"):
                ProgrammeExercise.objects.create(
                    day=cloned_day,
                    exercise_name=ex.exercise_name,
                    target_sets=ex.target_sets,
                    target_reps=ex.target_reps,
                    target_weight_kg=ex.target_weight_kg,
                    order=ex.order,
                )

        return cloned_block

    base_assignments = ClientProgramme.objects.filter(
        Q(block__parent_template=template_block) | Q(block=template_block)
    ).select_related("client", "block", "block__parent_template")

    owns_assignments = base_assignments.filter(trainer=request.user).exists()

    assignments_qs = base_assignments.filter(trainer=request.user)

    cp_param = request.GET.get("cp")
    if is_template_block:
        assignment = None
    else:
        if not owns_assignments:
            raise Http404("Programme not found")

        if cp_param and cp_param.isdigit():
            assignment = assignments_qs.filter(id=int(cp_param)).first()
        elif assignments_qs.exists():
            assignment = assignments_qs.order_by("-start_date", "-id").first()
            redirect_base = reverse_lazy(
                "accounts:trainer_programme_detail",
                kwargs={"block_id": template_block.id},
            )
            return redirect(f"{redirect_base}?cp={assignment.id}")

    if assignment and not assignment.block.parent_template_id:
        cloned_block = clone_programme_block(
            template_block,
            request.user,
            assignment.client,
        )
        assignment.block = cloned_block
        assignment.status = "active"
        if not assignment.start_date:
            assignment.start_date = timezone.now().date()
        assignment.save()

        redirect_base = reverse_lazy(
            "accounts:trainer_programme_detail",
            kwargs={"block_id": template_block.id},
        )
        return redirect(f"{redirect_base}?cp={assignment.id}")

    is_tailored = bool(
        assignment and assignment.block.parent_template_id == template_block.id
    )
    can_edit = is_tailored
    assignment_client = assignment.client if assignment else None
    if not is_template_block:
        tailored_client = assignment_client
    if not is_template_block:
        tailored_client = assignment_client

    tailored_block = assignment.block if assignment else None
    if tailored_block:
        tailored_days = tailored_block.days.all().order_by("order")
    else:
        tailored_days = ProgrammeDay.objects.none()

    day_param = request.GET.get("day")
    selected_day = None

    if tailored_days:
        if day_param and day_param.isdigit():
            selected_day = tailored_days.filter(id=int(day_param)).first()
        if selected_day is None:
            selected_day = tailored_days.first()

    if selected_day:
        exercises_qs = (
            ProgrammeExercise.objects.filter(day=selected_day)
            .select_related("day")
            .order_by("order")
        )
    else:
        exercises_qs = ProgrammeExercise.objects.none()

    exercise_formset = None

    # Only list clients that are assigned to this trainer for safety.
    if is_template_block:
        assigned_emails = ConsultationRequest.objects.filter(
            assigned_trainer=request.user,
            status=ConsultationRequest.STATUS_ASSIGNED,
        ).values_list("email", flat=True)

        allowed_email_set = {e.lower() for e in assigned_emails if e}
        assignable_clients = list(
            User.objects.filter(
                email__in=allowed_email_set,
                is_staff=False,
            ).order_by("first_name", "last_name", "username")
        )

    if (
        not is_template_block
        and request.method == "POST"
        and request.POST.get("action") == "delete"
    ):
        if not assignment or assignment.trainer != request.user:
            raise Http404("Programme not found")
        block.delete()
        messages.success(request, "Tailored programme deleted.")
        return redirect("accounts:trainer_programmes")

    if request.method == "POST" and "save_exercises" in request.POST:
        if not is_tailored:
            return HttpResponseForbidden(
                "Template programmes cannot be edited. Assign to a "
                "client first."
            )

        exercise_formset = ExerciseFormSet(
            request.POST,
            queryset=exercises_qs,
            prefix="ex",
        )

        if exercise_formset.is_valid():
            exercise_formset.save()
            messages.success(request, "Tailored programme updated.")

            redirect_url = reverse_lazy(
                "accounts:trainer_programme_detail",
                kwargs={"block_id": template_block.id},
            )
            query_bits = []
            if assignment:
                query_bits.append(f"cp={assignment.id}")
            if selected_day:
                query_bits.append(f"day={selected_day.id}")
            if query_bits:
                redirect_url = f"{redirect_url}?{'&'.join(query_bits)}"
            return redirect(redirect_url)

        messages.error(request, "Please correct the errors below.")

    elif (
        request.method == "POST"
        and not is_tailored
        and "convert_to_tailored" not in request.POST
    ):
        client_id = request.POST.get("assign_client_id") or request.POST.get(
            "client_id"
        )
        assign_clicked = (
            "assign_to_client" in request.POST
            or "assign_programme" in request.POST
            or bool(client_id)
        )

        if assign_clicked and client_id:
            client_user = get_object_or_404(User, id=client_id)

            allowed = request.user.is_superuser or (
                client_user.email
                and client_user.email.lower() in allowed_email_set
            )

            if not allowed:
                messages.error(
                    request,
                    "You are not allowed to assign this client.",
                )
                return redirect(
                    "accounts:trainer_programme_detail",
                    block_id=template_block.id,
                )

            existing_cp = ClientProgramme.objects.filter(
                client=client_user,
                block__parent_template=template_block,
            ).select_related("block").first()

            if existing_cp:
                messages.info(
                    request,
                    "Client already has a tailored copy. Opening it.",
                )
                redirect_base = reverse_lazy(
                    "accounts:trainer_programme_detail",
                    kwargs={"block_id": template_block.id},
                )
                return redirect(f"{redirect_base}?cp={existing_cp.id}")

            legacy_cp = ClientProgramme.objects.filter(
                client=client_user,
                block=template_block,
            ).select_related("block").first()

            if legacy_cp:
                cloned_block = clone_programme_block(
                    template_block,
                    request.user,
                    client_user,
                )
                legacy_cp.block = cloned_block
                legacy_cp.trainer = request.user
                legacy_cp.status = "active"
                if not legacy_cp.start_date:
                    legacy_cp.start_date = timezone.now().date()
                legacy_cp.save()
                messages.info(
                    request,
                    (
                        "Existing template assignment converted to a "
                        "tailored copy."
                    ),
                )
                redirect_base = reverse_lazy(
                    "accounts:trainer_programme_detail",
                    kwargs={"block_id": template_block.id},
                )
                return redirect(f"{redirect_base}?cp={legacy_cp.id}")

            cloned_block = clone_programme_block(
                template_block,
                request.user,
                client_user,
            )

            cp, created = ClientProgramme.objects.get_or_create(
                client=client_user,
                block=cloned_block,
                defaults={
                    "trainer": request.user,
                    "status": "active",
                    "start_date": timezone.now().date(),
                },
            )

            if not created:
                cp.trainer = request.user
                cp.status = "active"
                if not cp.start_date:
                    cp.start_date = timezone.now().date()
                cp.save()

            messages.success(
                request,
                "Tailored programme copy created and assigned to client.",
            )
            redirect_base = reverse_lazy(
                "accounts:trainer_programme_detail",
                kwargs={"block_id": template_block.id},
            )
            return redirect(f"{redirect_base}?cp={cp.id}")

    elif request.method == "POST" and "convert_to_tailored" in request.POST:
        if not assignment:
            return HttpResponseForbidden("No assignment selected.")

        if assignment.block.parent_template_id:
            messages.info(request, "This client already has a tailored copy.")
            redirect_base = reverse_lazy(
                "accounts:trainer_programme_detail",
                kwargs={"block_id": template_block.id},
            )
            return redirect(f"{redirect_base}?cp={assignment.id}")

        cloned_block = clone_programme_block(
            template_block,
            request.user,
            assignment.client,
        )
        assignment.block = cloned_block
        assignment.status = "active"
        if not assignment.start_date:
            assignment.start_date = timezone.now().date()
        assignment.save()

        messages.success(
            request,
            "Converted to tailored copy. You can now edit safely.",
        )

        redirect_base = reverse_lazy(
            "accounts:trainer_programme_detail",
            kwargs={"block_id": template_block.id},
        )
        return redirect(f"{redirect_base}?cp={assignment.id}")

    if request.method == "GET" and is_tailored:
        exercise_formset = ExerciseFormSet(queryset=exercises_qs, prefix="ex")

    filtered_template_days = template_days_qs
    if selected_day:
        filtered_template_days = template_days_qs.filter(
            order=selected_day.order
        )

    preview_days = []
    for day_obj in filtered_template_days:
        preview_days.append(
            {
                "day": day_obj,
                "exercises": day_obj.exercises.all().order_by("order"),
            }
        )

    context = {
        "block": template_block,
        "days": template_days_qs,
        "preview_days": preview_days,
        "assignable_clients": assignable_clients,
        "is_template_block": is_template_block,
        "tailored_client": tailored_client,
        "is_tailored": is_tailored,
        "can_edit": can_edit,
        "assignment_client": assignment_client,
        "assignment": assignment,
        "selected_day_id": selected_day.id if selected_day else None,
        "assignments": list(assignments_qs.order_by("client__username")),
        "selected_cp_id": assignment.id if assignment else None,
        "tailored_days": tailored_days,
        "exercise_formset": exercise_formset,
    }
    return render(request, "trainer/programme_detail.html", context)


@login_required(login_url="accounts:trainer_login")
@staff_required
def owner_programme_detail(request, block_id):
    """
    Owner view: show any programme block across all trainers/clients.
    Only superusers should access this route.
    """
    if not request.user.is_superuser:
        raise Http404("Owner view only")

    block = get_object_or_404(
        ProgrammeBlock.objects.prefetch_related(
            "days__exercises",
            "assignments",
        ),
        id=block_id,
    )

    template_block = block.parent_template if block.parent_template else block
    template_days_qs = (
        template_block.days.all()
        .order_by("order")
        .prefetch_related("exercises")
    )

    ExerciseFormSet = modelformset_factory(
        ProgrammeExercise,
        fields=("target_sets", "target_reps", "target_weight_kg"),
        extra=0,
    )

    def clone_programme_block(template_block_obj, trainer_user, client_user):
        """
        Deep clone ProgrammeBlock -> days -> exercises,
        so templates stay untouched.
        """
        cloned_block = ProgrammeBlock.objects.create(
            name=(
                f"{template_block_obj.name} "
                f"(Tailored for "
                f"{client_user.get_full_name() or client_user.username})"
            ),
            description=template_block_obj.description,
            weeks=template_block_obj.weeks,
            created_by=trainer_user,
            is_template=False,
            parent_template=template_block_obj,
        )

        for day in template_block_obj.days.all().order_by("order"):
            cloned_day = ProgrammeDay.objects.create(
                block=cloned_block,
                name=day.name,
                order=day.order,
            )

            for ex in day.exercises.all().order_by("order"):
                ProgrammeExercise.objects.create(
                    day=cloned_day,
                    exercise_name=ex.exercise_name,
                    target_sets=ex.target_sets,
                    target_reps=ex.target_reps,
                    target_weight_kg=ex.target_weight_kg,
                    order=ex.order,
                )

        return cloned_block

    trainer_filter = request.GET.get("trainer", "all")

    base_assignments = ClientProgramme.objects.filter(
        Q(block__parent_template=template_block) | Q(block=template_block)
    ).select_related("client", "block", "block__parent_template")

    trainer_options = (
        User.objects.filter(is_active=True, is_staff=True)
        .order_by("first_name", "last_name", "username")
    )

    # Filter assignments by trainer when requested to keep owner views scoped.
    assignments_qs = base_assignments
    if trainer_filter == "me":
        assignments_qs = assignments_qs.filter(trainer=request.user)
    elif trainer_filter.isdigit():
        assignments_qs = assignments_qs.filter(trainer_id=int(trainer_filter))

    cp_param = request.GET.get("cp")
    assignment = None

    if cp_param and cp_param.isdigit():
        # If selected client no longer matches trainer filter, fall back.
        assignment = assignments_qs.filter(id=int(cp_param)).first()

    if assignment is None and assignments_qs.exists():
        assignment = assignments_qs.order_by("-start_date", "-id").first()
        redirect_base = reverse_lazy(
            "accounts:owner_programme_detail",
            kwargs={"block_id": template_block.id},
        )
        query_bits = [f"trainer={trainer_filter}", f"cp={assignment.id}"]
        return redirect(f"{redirect_base}?{'&'.join(query_bits)}")

    if assignment and not assignment.block.parent_template_id:
        cloned_block = clone_programme_block(
            template_block,
            request.user,
            assignment.client,
        )
        assignment.block = cloned_block
        assignment.status = "active"
        if not assignment.start_date:
            assignment.start_date = timezone.now().date()
        assignment.save()

        redirect_base = reverse_lazy(
            "accounts:owner_programme_detail",
            kwargs={"block_id": template_block.id},
        )
        query_bits = [f"trainer={trainer_filter}", f"cp={assignment.id}"]
        return redirect(f"{redirect_base}?{'&'.join(query_bits)}")

    is_tailored = bool(
        assignment and assignment.block.parent_template_id == template_block.id
    )
    can_edit = is_tailored
    assignment_client = assignment.client if assignment else None

    tailored_block = assignment.block if assignment else None
    if tailored_block:
        tailored_days = tailored_block.days.all().order_by("order")
    else:
        tailored_days = ProgrammeDay.objects.none()

    day_param = request.GET.get("day")
    selected_day = None

    if tailored_days:
        if day_param and day_param.isdigit():
            selected_day = tailored_days.filter(id=int(day_param)).first()
        if selected_day is None:
            selected_day = tailored_days.first()

    if selected_day:
        exercises_qs = (
            ProgrammeExercise.objects.filter(day=selected_day)
            .select_related("day")
            .order_by("order")
        )
    else:
        exercises_qs = ProgrammeExercise.objects.none()

    exercise_formset = None

    # Owner dropdown should list clients in the filtered assignment set.
    assignment_clients = assignments_qs.values_list("client", flat=True)
    assignable_clients = list(
        User.objects.filter(id__in=assignment_clients)
        .order_by("username")
        .distinct()
    )
    allowed_email_set = {
        u.email.lower() for u in assignable_clients if u.email
    }

    if request.method == "POST" and "save_exercises" in request.POST:
        if not is_tailored:
            return HttpResponseForbidden(
                "Template programmes cannot be edited. Assign to a "
                "client first."
            )

        exercise_formset = ExerciseFormSet(
            request.POST,
            queryset=exercises_qs,
            prefix="ex",
        )

        if exercise_formset.is_valid():
            exercise_formset.save()
            messages.success(request, "Tailored programme updated.")

            redirect_url = reverse_lazy(
                "accounts:owner_programme_detail",
                kwargs={"block_id": template_block.id},
            )
            query_bits = [f"trainer={trainer_filter}"]
            if assignment:
                query_bits.append(f"cp={assignment.id}")
            if selected_day:
                query_bits.append(f"day={selected_day.id}")
            if query_bits:
                redirect_url = f"{redirect_url}?{'&'.join(query_bits)}"
            return redirect(redirect_url)

        messages.error(request, "Please correct the errors below.")

    elif (
        request.method == "POST"
        and not is_tailored
        and "convert_to_tailored" not in request.POST
    ):
        client_id = request.POST.get("assign_client_id") or request.POST.get(
            "client_id"
        )
        assign_clicked = (
            "assign_to_client" in request.POST
            or "assign_programme" in request.POST
            or bool(client_id)
        )

        if assign_clicked and client_id:
            client_user = get_object_or_404(User, id=client_id)

            allowed = client_user.email and (
                client_user.email.lower() in allowed_email_set
            )

            if not allowed:
                messages.error(
                    request,
                    "You are not allowed to assign this client.",
                )
                return redirect(
                    "accounts:owner_programme_detail",
                    block_id=template_block.id,
                )

            existing_cp = ClientProgramme.objects.filter(
                client=client_user,
                block__parent_template=template_block,
            ).select_related("block").first()

            if existing_cp:
                messages.info(
                    request,
                    "Client already has a tailored copy. Opening it.",
                )
                redirect_base = reverse_lazy(
                    "accounts:owner_programme_detail",
                    kwargs={"block_id": template_block.id},
                )
                query_bits = [f"trainer={trainer_filter}", f"cp={existing_cp.id}"]
                return redirect(f"{redirect_base}?{'&'.join(query_bits)}")

            legacy_cp = ClientProgramme.objects.filter(
                client=client_user,
                block=template_block,
            ).select_related("block").first()

            if legacy_cp:
                cloned_block = clone_programme_block(
                    template_block,
                    request.user,
                    client_user,
                )
                legacy_cp.block = cloned_block
                legacy_cp.trainer = request.user
                legacy_cp.status = "active"
                if not legacy_cp.start_date:
                    legacy_cp.start_date = timezone.now().date()
                legacy_cp.save()
                messages.info(
                    request,
                    (
                        "Existing template assignment converted to a "
                        "tailored copy."
                    ),
                )
                redirect_base = reverse_lazy(
                    "accounts:owner_programme_detail",
                    kwargs={"block_id": template_block.id},
                )
                query_bits = [f"trainer={trainer_filter}", f"cp={legacy_cp.id}"]
                return redirect(f"{redirect_base}?{'&'.join(query_bits)}")

            cloned_block = clone_programme_block(
                template_block,
                request.user,
                client_user,
            )

            cp, created = ClientProgramme.objects.get_or_create(
                client=client_user,
                block=cloned_block,
                defaults={
                    "trainer": request.user,
                    "status": "active",
                    "start_date": timezone.now().date(),
                },
            )

            if not created:
                cp.trainer = request.user
                cp.status = "active"
                if not cp.start_date:
                    cp.start_date = timezone.now().date()
                cp.save()

            messages.success(
                request,
                "Tailored programme copy created and assigned to client.",
            )
            redirect_base = reverse_lazy(
                "accounts:owner_programme_detail",
                kwargs={"block_id": template_block.id},
            )
            query_bits = [f"trainer={trainer_filter}", f"cp={cp.id}"]
            return redirect(f"{redirect_base}?{'&'.join(query_bits)}")

    elif request.method == "POST" and "convert_to_tailored" in request.POST:
        if not assignment:
            return HttpResponseForbidden("No assignment selected.")

        if assignment.block.parent_template_id:
            messages.info(request, "This client already has a tailored copy.")
            redirect_base = reverse_lazy(
                "accounts:owner_programme_detail",
                kwargs={"block_id": template_block.id},
            )
            query_bits = [f"trainer={trainer_filter}", f"cp={assignment.id}"]
            return redirect(f"{redirect_base}?{'&'.join(query_bits)}")

        cloned_block = clone_programme_block(
            template_block,
            request.user,
            assignment.client,
        )
        assignment.block = cloned_block
        assignment.status = "active"
        if not assignment.start_date:
            assignment.start_date = timezone.now().date()
        assignment.save()

        messages.success(
            request,
            "Converted to tailored copy. You can now edit safely.",
        )

        redirect_base = reverse_lazy(
            "accounts:owner_programme_detail",
            kwargs={"block_id": template_block.id},
        )
        query_bits = [f"trainer={trainer_filter}", f"cp={assignment.id}"]
        return redirect(f"{redirect_base}?{'&'.join(query_bits)}")

    if request.method == "GET" and is_tailored:
        exercise_formset = ExerciseFormSet(queryset=exercises_qs, prefix="ex")

    filtered_template_days = template_days_qs
    if selected_day:
        filtered_template_days = template_days_qs.filter(
            order=selected_day.order
        )

    preview_days = []
    for day_obj in filtered_template_days:
        preview_days.append(
            {
                "day": day_obj,
                "exercises": day_obj.exercises.all().order_by("order"),
            }
        )

    context = {
        "block": template_block,
        "days": template_days_qs,
        "preview_days": preview_days,
        "assignable_clients": assignable_clients,
        "trainer_filter": trainer_filter,
        "trainer_options": trainer_options,
        "is_tailored": is_tailored,
        "can_edit": can_edit,
        "assignment_client": assignment_client,
        "assignment": assignment,
        "selected_day_id": selected_day.id if selected_day else None,
        "assignments": list(assignments_qs.order_by("client__username")),
        "selected_cp_id": assignment.id if assignment else None,
        "tailored_days": tailored_days,
        "exercise_formset": exercise_formset,
    }
    return render(request, "owner/programme_detail.html", context)


@login_required
@staff_member_required
def trainer_programmes(request):
    """
    Trainer view: high-level overview of programme blocks and templates.
    Now driven by ProgrammeBlock records instead of static data.
    """
    if request.user.is_superuser:
        active_blocks_qs = ProgrammeBlock.objects.filter(
            is_template=False,
            assignments__isnull=False,
        ).distinct()
    else:
        active_blocks_qs = ProgrammeBlock.objects.filter(
            is_template=False,
            assignments__trainer=request.user,
        ).distinct()

    programme_blocks = []
    for block in active_blocks_qs.select_related("parent_template"):
        trainer_assignments = block.assignments.all()
        if not request.user.is_superuser:
            trainer_assignments = trainer_assignments.filter(
                trainer=request.user
            )

        first_cp = trainer_assignments.order_by("-start_date", "-id").first()

        programme_blocks.append(
            {
                "block": block,
                "cp_id": first_cp.id if first_cp else None,
                "clients": trainer_assignments.count(),
                "phase": f"Weeks 1-{block.weeks}",
                "status": "Active",
                "next_action": "Review check-ins",
            }
        )

    template_blocks_qs = (
        ProgrammeBlock.objects.filter(is_template=True)
        .annotate(assignments_count=Count("assignments"))
        .filter(assignments_count=0)
        .distinct()
    )

    programme_templates = [
        {
            "id": block.id,
            "name": block.name,
            "focus": block.description or "-",
            "length": f"{block.weeks} weeks",
        }
        for block in template_blocks_qs
    ]

    context = {
        "programme_blocks": programme_blocks,
        "programme_templates": programme_templates,
    }
    # Owners see owner-branded template; trainers see trainer template.
    template = (
        "owner/programmes.html"
        if request.user.is_superuser
        else "trainer/programmes.html"
    )
    return render(request, template, context)


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_consultation_detail(request, pk):
    """
    Detail view for a consultation request with assign-to-me action.
    """
    consultation = get_object_or_404(ConsultationRequest, pk=pk)

    if request.method == "POST" and "assign_to_me" in request.POST:
        result = assign_consultation_to_trainer(
            request=request,
            consultation=consultation,
            trainer_user=request.user,
        )
        level = getattr(messages, result["message_level"].upper(), messages.INFO)
        messages.add_message(request, level, result["message"])
        return redirect(result["redirect"])

    return render(
        request,
        "trainer/consultation_detail.html",
        {"consultation": consultation},
    )


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_client_detail(request, client_id):
    """Trainer-facing overview of a single client's workouts and metrics."""
    trainer = request.user
    client_user = get_object_or_404(User, id=client_id)

    has_assignment = ConsultationRequest.objects.filter(
        assigned_trainer=trainer,
        email__iexact=client_user.email,
    ).exists()

    if not (has_assignment or trainer.is_superuser):
        return HttpResponseForbidden("Not allowed to view this client.")

    action = request.POST.get("action", "").strip().lower()
    if request.method == "POST" and action in {"update", "delete"}:
        entry_id = request.POST.get("entry_id")
        entry = get_object_or_404(
            BodyMetricEntry,
            id=entry_id,
            client=client_user,
        )

        if action == "delete":
            entry.delete()
            messages.success(request, "Check-in deleted.")
            return redirect(
                "accounts:trainer_client_detail",
                client_id=client_user.id,
            )

        form = BodyMetricEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Check-in updated.")
            return redirect(
                "accounts:trainer_client_detail",
                client_id=client_user.id,
            )

    workouts = WorkoutSession.objects.filter(client=client_user).order_by(
        "-date",
        "-id",
    )[:5]

    entries_qs = BodyMetricEntry.objects.filter(
        client=client_user
    ).order_by("date")
    entries = list(entries_qs)

    chart_labels = [entry.date.strftime("%d %b") for entry in entries]
    bodyweight_values = []
    bench_values = []

    for entry in entries:
        bw = entry.bodyweight_kg
        bt = entry.bench_top_set_kg
        bodyweight_values.append(float(bw) if bw is not None else None)
        bench_values.append(float(bt) if bt is not None else None)

    has_bodyweight_data = any(v is not None for v in bodyweight_values)
    has_bench_data = any(v is not None for v in bench_values)

    recent_entries = BodyMetricEntry.objects.filter(
        client=client_user
    ).order_by(
        "-date",
        "-created_at",
    )[:5]

    latest = entries_qs.order_by("-date", "-created_at").first()
    four_weeks_ago = timezone.now().date() - datetime.timedelta(weeks=4)
    earlier = entries_qs.filter(date__lte=four_weeks_ago).order_by(
        "-date",
        "-created_at",
    ).first()

    def latest_or_dash(entry, field, suffix=""):
        if entry is None:
            return "—"
        val = getattr(entry, field, None)
        if val is None:
            return "—"
        return f"{val}{suffix}"

    def change_or_dash(lat_entry, early_entry, field, suffix=""):
        if lat_entry is None or early_entry is None:
            return "—"
        lat_val = getattr(lat_entry, field, None)
        early_val = getattr(early_entry, field, None)
        if lat_val is None or early_val is None:
            return "—"
        diff = lat_val - early_val
        sign = "+" if diff > 0 else ""
        if suffix.strip() == "h":
            formatted = f"{diff:.2f}"
        else:
            formatted = f"{diff:.1f}"
        return f"{sign}{formatted}{suffix}"

    summary_rows = [
        {
            "label": "Bodyweight",
            "latest": latest_or_dash(latest, "bodyweight_kg", " kg"),
            "change": change_or_dash(latest, earlier, "bodyweight_kg", " kg"),
            "target": "77.5 kg",
        },
        {
            "label": "Waist",
            "latest": latest_or_dash(latest, "waist_cm", " cm"),
            "change": change_or_dash(latest, earlier, "waist_cm", " cm"),
            "target": "82 cm",
        },
        {
            "label": "Bench top set",
            "latest": latest_or_dash(latest, "bench_top_set_kg", " kg"),
            "change": change_or_dash(
                latest,
                earlier,
                "bench_top_set_kg",
                " kg",
            ),
            "target": "62.5 kg x 8",
        },
        {
            "label": "Sleep average",
            "latest": latest_or_dash(latest, "sleep_hours", " h"),
            "change": change_or_dash(latest, earlier, "sleep_hours", " h"),
            "target": "7.5 h",
        },
    ]

    context = {
        "trainer": trainer,
        "client": client_user,
        "workouts": workouts,
        "recent_entries": recent_entries,
        "summary_rows": summary_rows,
        "chart_labels_json": json.dumps(chart_labels),
        "bodyweight_series_json": json.dumps(bodyweight_values),
        "bench_series_json": json.dumps(bench_values),
        "has_bodyweight_data": has_bodyweight_data,
        "has_bench_data": has_bench_data,
    }
    return render(request, "trainer/client_detail.html", context)


@login_required(login_url="accounts:trainer_login")
def owner_delete_client(request, client_id):
    """
    Allow owner (superuser) to hard-delete a client and related records.
    Trainers must never see this action.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only owners can delete clients.")

    client_user = get_object_or_404(User, id=client_id)

    # Block deleting staff, other owners, or yourself.
    if client_user.is_staff or client_user.is_superuser or client_user == request.user:
        messages.error(request, "You cannot delete this account.")
        return redirect("accounts:trainer_client_detail", client_id=client_id)

    if request.method != "POST":
        return HttpResponseForbidden("Invalid request method.")

    with transaction.atomic():
        # Remove any consultation requests tied to this email to avoid stale rows.
        if client_user.email:
            ConsultationRequest.objects.filter(
                email__iexact=client_user.email
            ).delete()
        # Deleting the User will cascade to ClientProfile and related FK data.
        client_user.delete()

    messages.success(request, "Client account deleted.")
    return redirect("accounts:trainer_clients")


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_session_edit(request, session_id):
    """Allow a trainer to tweak a client's workout session (notes only)."""
    session = get_object_or_404(WorkoutSession, id=session_id)
    trainer = request.user

    has_assignment = ConsultationRequest.objects.filter(
        assigned_trainer=trainer,
        email__iexact=session.client.email,
    ).exists()

    if not (has_assignment or trainer.is_superuser):
        return HttpResponseForbidden("Not allowed to edit this session.")

    if request.method == "POST":
        form = TrainerWorkoutSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Session updated.")
            return redirect(
                "accounts:trainer_client_detail",
                client_id=session.client_id,
            )
    else:
        form = TrainerWorkoutSessionForm(instance=session)

    return render(
        request,
        "trainer/session_edit.html",
        {
            "trainer": trainer,
            "client": session.client,
            "session": session,
            "form": form,
        },
    )
