# accounts/views.py

from collections import OrderedDict
import datetime
import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden

from training.forms import WorkoutSessionForm, BodyMetricEntryForm
from training.models import ConsultationRequest, WorkoutSession, BodyMetricEntry
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class TrainerWorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ["notes"]
from .models import ClientProfile




class TrainerLoginView(LoginView):

    """

    Trainer / owner login using Django's built-in authentication.

    """

    template_name = "accounts/trainer_login.html"



    def get_success_url(self):

        # After login, go to the trainer dashboard

        return reverse_lazy("accounts:trainer_dashboard")





class ClientLoginView(LoginView):

    """

    Client login using Django's built-in authentication.

    """

    template_name = "accounts/client_login.html"



    def get_success_url(self):

        # After login, go to the client dashboard

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



    context = {

        "profile": profile,

        "latest_sessions": [],

        "latest_metrics": [],

    }

    return render(request, "client/dashboard.html", context)





@login_required

def client_today(request):

    """Display the current day's training plan for the logged-in client."""

    return render(request, "client/today.html")





@login_required

def client_programme_library(request):
    """
    Client view: show current training block and sessions.
    Uses static demo data for now.
    """
    programme = {
        "name": "Hypertrophy Block (6 weeks)",
        "current_week": 3,
        "weeks": [1, 2, 3, 4, 5, 6],
        "sessions": [
            {"day": "Day 1 - Upper", "summary": "Bench, Row, Accessories", "cta": "Open"},
            {"day": "Day 2 - Lower", "summary": "Squat, RDL, Core", "cta": "Open"},
            {"day": "Day 3 - Full", "summary": "Press, Pull, Conditioning", "cta": "View"},
        ],
    }

    context = {"programme": programme}
    return render(request, "client/programme_library.html", context)





@login_required
def client_workout_log(request):
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    recent_sessions = (
        WorkoutSession.objects.filter(client=request.user)
        .order_by("-date", "-created_at")[:20]
    )

    if request.method == "POST":
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Set inputs
            bench_set1 = cd.get("bench_set1")
            bench_set2 = cd.get("bench_set2")
            bench_set3 = cd.get("bench_set3")

            row_set1 = cd.get("row_set1")
            row_set2 = cd.get("row_set2")
            row_set3 = cd.get("row_set3")

            incline_set1 = cd.get("incline_set1")
            incline_set2 = cd.get("incline_set2")
            incline_set3 = cd.get("incline_set3")

            # Weight inputs (not part of the form)
            bench_weight_raw = (request.POST.get("bench_weight") or "").strip()
            row_weight_raw = (request.POST.get("row_weight") or "").strip()
            incline_weight_raw = (request.POST.get("incline_weight") or "").strip()

            def format_sets(*vals):
                return " | ".join(v or "—" for v in vals)

            def format_weight(raw_val):
                return f"{raw_val}kg" if raw_val else "—"


            bench_sets_display = format_sets(bench_set1, bench_set2, bench_set3)
            row_sets_display = format_sets(row_set1, row_set2, row_set3)
            incline_sets_display = format_sets(
                incline_set1,
                incline_set2,
                incline_set3,
            )

            session_details_lines = [
                "Session details:",
                (
                    f"Bench Press ({format_weight(bench_weight_raw)}): "
                    f"{bench_sets_display}"
                ),
                (
                    f"Seated Row ({format_weight(row_weight_raw)}): "
                    f"{row_sets_display}"
                ),
                (
                    f"DB Incline ({format_weight(incline_weight_raw)}): "
                    f"{incline_sets_display}"
                ),
            ]

            base_notes = cd.get("notes") or ""
            session_notes = "\n\n".join(
                part for part in (base_notes, "\n".join(session_details_lines)) if part
            )

            session = form.save(commit=False)

            if not session.date:
                session.date = timezone.localdate()

            if getattr(session, "client_id", None) is None:
                session.client = request.user

            if hasattr(session, "status") and not getattr(session, "status", None):
                try:
                    session.status = "logged"
                except Exception:
                    pass

            session.notes = session_notes
            session.save()

            messages.success(request, "Workout session saved.")
            return redirect("accounts:client_workout_log")
    else:
        form = WorkoutSessionForm()

    context = {
        "sessions": recent_sessions,
        "session_form": form,
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

    session = get_object_or_404(WorkoutSession, pk=session_id, client=request.user)

    name = (request.POST.get("name") or "").strip()
    if name:
        session.name = name

    if hasattr(session, "status"):
        status_val = (request.POST.get("status") or "").strip()
        if status_val:
            session.status = status_val

    if "notes" in request.POST:
        session.notes = request.POST.get("notes", "")

    session.save()
    messages.success(request, "Workout session updated.")
    return redirect("accounts:client_workout_log")




@login_required
def client_metrics(request):
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    user = request.user

    if request.method == "POST":
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
            "target_display": "62.5 kg ï¿½- 8",
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

    recent_entries = (
        BodyMetricEntry.objects.filter(client=user)
        .order_by("-date", "-created_at")[:5]
    )

    # Chart data: all entries ordered by date
    chart_entries = BodyMetricEntry.objects.filter(client=user).order_by("date")
    chart_labels = [entry.date.strftime("%d %b") for entry in chart_entries]

    bodyweight_series = [
        float(entry.bodyweight_kg) if entry.bodyweight_kg is not None else None
        for entry in chart_entries
    ]

    bench_series = [
        float(entry.bench_top_set_kg) if entry.bench_top_set_kg is not None else None
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

def client_check_ins(request):

    if request.user.is_staff:

        return redirect("accounts:trainer_dashboard")

    return render(request, "client/check_ins.html")





@login_required

def client_documents(request):

    if request.user.is_staff:

        return redirect("accounts:trainer_dashboard")



    return render(request, "client/documents.html")





@login_required

def client_support(request):

    if request.user.is_staff:

        return redirect("accounts:trainer_dashboard")



    if request.method == "POST":

        subject = request.POST.get("subject", "").strip()

        message = request.POST.get("message", "").strip()



        if subject and message:

            messages.success(

                request,

                "Support message sent. A coach will respond soon.",

            )

            return redirect("accounts:client_support")



        messages.error(request, "Both subject and message are required.")



    return render(request, "client/support.html")





def is_trainer(user):

    """

    For now we'll treat Django's is_staff flag as 'trainer / owner'.



    Later we can upgrade this to Groups or custom roles

    without changing the rest of the code.

    """

    return user.is_staff





def staff_required(view_func):

    return user_passes_test(

        lambda u: u.is_staff,

        login_url="accounts:trainer_login",

    )(view_func)





@login_required(login_url="accounts:trainer_login")

@staff_required

def trainer_dashboard(request):

    """

    Trainer dashboard:

    - Shows latest consultation requests

    - Includes a small stats summary pulled from the database

    """

    # Latest 4 consultation requests

    latest_requests = ConsultationRequest.objects.order_by("-created_at")[:4]



    # Total number of requests

    total_requests = ConsultationRequest.objects.count()



    # Breakdown by coaching option (e.g. 1:1 PT, Small Group, etc.)

    coaching_breakdown = (

        ConsultationRequest.objects.values("coaching_option")

        .annotate(count=Count("id"))

        .order_by("coaching_option")

    )



    # Map codes like "1to1" -> "1:1 Personal Training"

    choice_labels = dict(ConsultationRequest.COACHING_OPTION_CHOICES)

    for row in coaching_breakdown:

        row["label"] = choice_labels.get(

            row["coaching_option"],

            "Not specified",

        )



    context = {

        "latest_requests": latest_requests,

        "total_requests": total_requests,

        "coaching_breakdown": coaching_breakdown,

    }

    return render(request, "trainer/dashboard.html", context)





# Trainer side-menu stubs

@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_clients(request):
    """Show one row per email for the trainer's assigned clients."""
    trainer = request.user

    qs = (
        ConsultationRequest.objects.filter(assigned_trainer=trainer)
        .order_by("-created_at")
    )

    latest_by_email = {}
    for req in qs:
        key = (req.email or "").lower()
        if key and key not in latest_by_email:
            latest_by_email[key] = req

    latest_requests = sorted(
        latest_by_email.values(),
        key=lambda r: r.created_at,
        reverse=True,
    )

    rows = []
    for req in latest_requests:
        full_name = f"{req.first_name} {req.last_name}".strip() or req.email
        portal_user = User.objects.filter(email__iexact=req.email).first()

        rows.append(
            {
                "name": full_name,
                "email": req.email,
                "goal": req.training_goal,
                "coaching_option": req.coaching_option,
                "last_request_date": req.created_at.date(),
                "user_id": portal_user.id if portal_user else None,
            }
        )

    context = {
        "trainer": trainer,
        "clients": rows,
        "section": "clients",
    }
    return render(request, "trainer/clients.html", context)





@login_required(login_url="accounts:trainer_login")

@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_metrics(request):
    """
    Trainer view: overview of latest body metric entries per client.
    """
    # Later this can filter by clients assigned to this trainer.
    entries = (
        BodyMetricEntry.objects.select_related("client")
        .order_by("client__id", "-date")
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

    return render(
        request,
        "trainer/metrics.html",
        {
            "client_rows": client_rows,
        },
    )

@login_required
@staff_member_required
def trainer_programmes(request):
    """

    Trainer view: high-level overview of programme blocks and templates.

    Data is static sample content for now.

    """

    programme_blocks = [

        {

            "name": "Hypertrophy block (6 weeks)",

            "phase": "Weeks 1-6",

            "clients": 5,

            "status": "Active",

            "next_action": "Review week-3 check-ins",

        },

        {

            "name": "Strength foundation (4 weeks)",

            "phase": "Weeks 1-4",

            "clients": 3,

            "status": "Planning",

            "next_action": "Assign to new consultation requests",

        },

    ]



    programme_templates = [

        {

            "name": "General strength - 3 days",

            "focus": "Full-body strength",

            "length": "8 weeks",

        },

        {

            "name": "Fat-loss circuit - 2 days",

            "focus": "Conditioning / cardio",

            "length": "6 weeks",

        },

    ]



    context = {

        "programme_blocks": programme_blocks,

        "programme_templates": programme_templates,

    }
    return render(request, "trainer/programmes.html", context)






@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_consultation_detail(request, pk):
    """
    Detail view for a consultation request with assign-to-me action.
    """
    consultation = get_object_or_404(ConsultationRequest, pk=pk)

    if request.method == "POST" and "assign_to_me" in request.POST:
        if (
            consultation.assigned_trainer
            and consultation.assigned_trainer != request.user
            and not request.user.is_superuser
        ):
            messages.error(
                request,
                "This consultation is already assigned to another trainer.",
            )
        else:
            consultation.assigned_trainer = request.user
            consultation.save()
            messages.success(
                request,
                "Client has been added to the trainer client list.",
            )
        return redirect("accounts:trainer_clients")

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

    workouts = (
        WorkoutSession.objects.filter(client=client_user)
        .order_by("-date", "-id")[:5]
    )

    entries_qs = BodyMetricEntry.objects.filter(client=client_user).order_by("date")
    entries = list(entries_qs)

    chart_labels = [e.date.strftime("%d %b") for e in entries]
    bodyweight_values = [float(e.bodyweight_kg) if e.bodyweight_kg is not None else None for e in entries]
    bench_values = [float(e.bench_top_set_kg) if e.bench_top_set_kg is not None else None for e in entries]

    has_bodyweight_data = any(v is not None for v in bodyweight_values)
    has_bench_data = any(v is not None for v in bench_values)

    recent_entries = (
        BodyMetricEntry.objects.filter(client=client_user)
        .order_by("-date", "-created_at")[:5]
    )

    latest = entries_qs.order_by("-date", "-created_at").first()
    four_weeks_ago = timezone.now().date() - datetime.timedelta(weeks=4)
    earlier = (
        entries_qs.filter(date__lte=four_weeks_ago)
        .order_by("-date", "-created_at")
        .first()
    )

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
        formatted = f"{diff:.2f}" if suffix.strip() == "h" else f"{diff:.1f}"
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
            "change": change_or_dash(latest, earlier, "bench_top_set_kg", " kg"),
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
@staff_required
def trainer_session_edit(request, session_id):
    """Allow a trainer to tweak a client's workout session (status/notes)."""
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
            return redirect("accounts:trainer_client_detail", client_id=session.client_id)
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


