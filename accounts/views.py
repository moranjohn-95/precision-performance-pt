# accounts/views.py

from collections import OrderedDict
import datetime
import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden

from django.contrib.auth import get_user_model
from django import forms
from django.forms import modelformset_factory

from training.forms import WorkoutSessionForm, BodyMetricEntryForm
from training.models import (
    ConsultationRequest,
    WorkoutSession,
    BodyMetricEntry,
    ClientProgramme,
    ProgrammeBlock,
    ProgrammeDay,
    ProgrammeExercise,
)

from .models import ClientProfile

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
    if request.user.is_staff:
        return redirect("accounts:trainer_dashboard")

    initial = {}
    session_name_param = (request.GET.get("session_name") or "").strip()
    if session_name_param:
        # Your WorkoutSessionForm uses "name" (not session_name)
        initial["name"] = session_name_param

    programme_day = None
    programme_exercises = []

    # Optional: Try match ProgrammeDay by name ONLY if user has that block assigned
    if session_name_param:
        day_qs = (
            ProgrammeDay.objects.filter(name=session_name_param)
            .select_related("block")
        )
        for day in day_qs:
            if ClientProgramme.objects.filter(
                client=request.user,
                status="active",
                block=day.block,
            ).exists():
                programme_day = day
                programme_exercises = list(day.exercises.all().order_by("order"))
                break

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
            incline_sets_display = format_sets(incline_set1, incline_set2, incline_set3)

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

            # If model has status, set it (safe)
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
        form = WorkoutSessionForm(initial=initial)

    context = {
        "sessions": recent_sessions,
        "session_form": form,
        "programme_day": programme_day,
        "programme_exercises": programme_exercises,
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

    entries_qs = BodyMetricEntry.objects.filter(client=user).order_by("date", "created_at")
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
        {"label": "Bodyweight", "field": "bodyweight_kg", "unit": "kg", "target_display": "77.5 kg"},
        {"label": "Waist", "field": "waist_cm", "unit": "cm", "target_display": "82 cm"},
        {
            "label": "Bench top set",
            "field": "bench_top_set_kg",
            "unit": "kg",
            # ✅ FIXED unicode issue:
            "target_display": "62.5 kg x 8",
        },
        {"label": "Sleep average", "field": "sleep_hours", "unit": "h", "target_display": "7.5 h"},
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

    recent_entries = BodyMetricEntry.objects.filter(client=user).order_by("-date", "-created_at")[:5]

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
            messages.success(request, "Support message sent. A coach will respond soon.")
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
    return user_passes_test(lambda u: u.is_staff, login_url="accounts:trainer_login")(view_func)


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_dashboard(request):
    """
    Trainer dashboard:
    - Shows latest consultation requests
    - Includes a small stats summary pulled from the database
    """
    latest_requests = ConsultationRequest.objects.order_by("-created_at")[:4]
    total_requests = ConsultationRequest.objects.count()

    coaching_breakdown = (
        ConsultationRequest.objects.values("coaching_option")
        .annotate(count=Count("id"))
        .order_by("coaching_option")
    )

    choice_labels = dict(ConsultationRequest.COACHING_OPTION_CHOICES)
    for row in coaching_breakdown:
        row["label"] = choice_labels.get(row["coaching_option"], "Not specified")

    context = {
        "latest_requests": latest_requests,
        "total_requests": total_requests,
        "coaching_breakdown": coaching_breakdown,
    }
    return render(request, "trainer/dashboard.html", context)


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_clients(request):
    """Show one row per email for the trainer's assigned clients."""
    trainer = request.user

    qs = ConsultationRequest.objects.filter(assigned_trainer=trainer).order_by("-created_at")

    latest_by_email = {}
    for req in qs:
        key = (req.email or "").lower()
        if key and key not in latest_by_email:
            latest_by_email[key] = req

    latest_requests = sorted(latest_by_email.values(), key=lambda r: r.created_at, reverse=True)

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
@staff_required
def trainer_metrics(request):
    """
    Trainer view: overview of latest body metric entries per client.
    """
    entries = BodyMetricEntry.objects.select_related("client").order_by("client__id", "-date")

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

    return render(request, "trainer/metrics.html", {"client_rows": client_rows})


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

    template_block = block.parent_template if block.parent_template else block

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

    assignments_qs = (
        base_assignments
        if request.user.is_superuser
        else base_assignments.filter(trainer=request.user)
    )

    cp_param = request.GET.get("cp")
    assignment = None

    if cp_param and cp_param.isdigit():
        assignment = get_object_or_404(assignments_qs, id=int(cp_param))
    elif assignments_qs.exists():
        assignment = assignments_qs.order_by("-start_date", "-id").first()
        redirect_base = reverse_lazy(
            "accounts:trainer_programme_detail",
            kwargs={"block_id": template_block.id},
        )
        return redirect(f"{redirect_base}?cp={assignment.id}")

    # If a legacy assignment points directly to the template, convert it
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

    # Day selection for the tailored block
    tailored_block = assignment.block if assignment else None
    tailored_days = (
        tailored_block.days.all().order_by("order")
        if tailored_block
        else ProgrammeDay.objects.none()
    )
    day_param = request.GET.get("day")
    selected_day = None
    if tailored_days:
        if day_param and day_param.isdigit():
            selected_day = tailored_days.filter(id=int(day_param)).first()
        if selected_day is None:
            selected_day = tailored_days.first()

    exercises_qs = ProgrammeExercise.objects.none()
    if selected_day:
        exercises_qs = (
            ProgrammeExercise.objects.filter(day=selected_day)
            .select_related("day")
            .order_by("order")
        )

    exercise_formset = None

    # Determine assignable clients for this trainer
    if request.user.is_superuser:
        assignable_clients = list(
            User.objects.filter(is_staff=False).order_by("username")
        )
        allowed_email_set = {
            u.email.lower() for u in assignable_clients if u.email
        }
    else:
        assigned_emails = ConsultationRequest.objects.filter(
            assigned_trainer=request.user
        ).values_list("email", flat=True)

        allowed_email_set = {e.lower() for e in assigned_emails if e}
        assignable_clients = list(
            User.objects.filter(
                email__in=allowed_email_set
            ).order_by("username")
        )

    # ----------------------------
    # POST #1: Save tailored edits
    # ----------------------------
    if request.method == "POST" and "save_exercises" in request.POST:
        if not is_tailored:
            return HttpResponseForbidden(
                "Template programmes cannot be edited. "
                "Assign to a client first."
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

    # ----------------------------
    # POST #2: Assign programme (clone + assign)
    # ----------------------------
    elif (
        request.method == "POST"
        and not is_tailored
        and "convert_to_tailored" not in request.POST
    ):
        # Support BOTH naming conventions to avoid breaking template
        client_id = (
            request.POST.get("assign_client_id")
            or request.POST.get("client_id")
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

            # If a tailored copy already exists, reuse it
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

            # Clone the programme before assigning, so template stays unchanged
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

    # ----------------------------
    # POST #3: Convert legacy assignment to tailored copy
    # ----------------------------
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

    # GET: show formset if editable
    if request.method == "GET" and is_tailored:
        exercise_formset = ExerciseFormSet(queryset=exercises_qs, prefix="ex")

    template_days_qs = template_block.days.all().order_by("order").prefetch_related(
        "exercises"
    )
    if selected_day:
        template_days_qs = template_days_qs.filter(order=selected_day.order)

    preview_days = []
    for d in template_days_qs:
        preview_days.append(
            {
                "day": d,
                "exercises": d.exercises.all().order_by("order"),
            }
        )

    context = {
        "block": template_block,
        "days": template_block.days.all().order_by("order"),
        "preview_days": preview_days,
        "assignable_clients": assignable_clients,
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


@login_required
@staff_member_required
def trainer_programmes(request):
    """
    Trainer view: high-level overview of programme blocks and templates.
    Now driven by ProgrammeBlock records instead of static data.
    """
    assignments = (
        ClientProgramme.objects.select_related(
            "block",
            "block__parent_template",
        )
        if request.user.is_superuser
        else ClientProgramme.objects.select_related(
            "block",
            "block__parent_template",
        ).filter(trainer=request.user)
    )

    programme_blocks = []
    for cp in assignments:
        block = cp.block
        programme_blocks.append(
            {
                "id": cp.id,
                "block": block,
                "clients": block.assignments.count(),
                "phase": f"Weeks 1-{block.weeks}",
                "status": "Active",
                "next_action": "Review check-ins",
            }
        )

    programme_templates = [
        {
            "id": block.id,
            "name": block.name,
            "focus": block.description or "—",
            "length": f"{block.weeks} weeks",
        }
        for block in ProgrammeBlock.objects.filter(is_template=True)
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
            messages.error(request, "This consultation is already assigned to another trainer.")
        else:
            consultation.assigned_trainer = request.user
            consultation.save()
            messages.success(request, "Client has been added to the trainer client list.")
        return redirect("accounts:trainer_clients")

    return render(request, "trainer/consultation_detail.html", {"consultation": consultation})


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

    workouts = WorkoutSession.objects.filter(client=client_user).order_by("-date", "-id")[:5]

    entries_qs = BodyMetricEntry.objects.filter(client=client_user).order_by("date")
    entries = list(entries_qs)

    chart_labels = [e.date.strftime("%d %b") for e in entries]
    bodyweight_values = [
        float(e.bodyweight_kg) if e.bodyweight_kg is not None else None for e in entries
    ]
    bench_values = [
        float(e.bench_top_set_kg) if e.bench_top_set_kg is not None else None for e in entries
    ]

    has_bodyweight_data = any(v is not None for v in bodyweight_values)
    has_bench_data = any(v is not None for v in bench_values)

    recent_entries = BodyMetricEntry.objects.filter(client=client_user).order_by("-date", "-created_at")[:5]

    latest = entries_qs.order_by("-date", "-created_at").first()
    four_weeks_ago = timezone.now().date() - datetime.timedelta(weeks=4)
    earlier = entries_qs.filter(date__lte=four_weeks_ago).order_by("-date", "-created_at").first()

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
