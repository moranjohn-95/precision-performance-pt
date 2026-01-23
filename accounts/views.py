# accounts/views.py
from collections import OrderedDict

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from training.models import ConsultationRequest
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
            {
                "day": "Day 1 — Upper",
                "summary": "Bench, Row, Accessories",
                "cta": "Open",
            },
            {
                "day": "Day 2 — Lower",
                "summary": "Squat, RDL, Core",
                "cta": "Open",
            },
            {
                "day": "Day 3 — Full",
                "summary": "Press, Pull, Conditioning",
                "cta": "View",
            },
        ],
    }

    context = {"programme": programme}
    return render(request, "client/programme_library.html", context)


@login_required
def client_workout_log(request):
    """
    Display the workout log page for a client.
    """
    sample_sessions = [
        {
            "name": "Day 1 — Upper",
            "date": "Mon",
            "status": "Logged",
            "notes": "Bench, row, accessories.",
        },
        {
            "name": "Day 2 — Lower",
            "date": "Wed",
            "status": "Planned",
            "notes": "Squat, RDL, core.",
        },
        {
            "name": "Day 3 — Full",
            "date": "Fri",
            "status": "Saved draft",
            "notes": "Press, pull, conditioning.",
        },
    ]

    context = {"sessions": sample_sessions}
    return render(request, "client/workout_log.html", context)


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
    """
    Simple view of potential clients derived from consultation requests.
    Groups requests by email so each client appears once.
    """
    qs = ConsultationRequest.objects.order_by(
        "last_name",
        "first_name",
        "-created_at",
    )

    unique_by_email = OrderedDict()
    for req in qs:
        if req.email not in unique_by_email:
            unique_by_email[req.email] = req

    clients = list(unique_by_email.values())

    context = {
        "clients": clients,
        "section": "clients",
    }
    return render(request, "trainer/clients.html", context)


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_programmes(request):
    """
    Placeholder for trainer programme management.
    """
    return render(request, "trainer/programmes.html")


@login_required(login_url="accounts:trainer_login")
@staff_required
def trainer_metrics(request):
    """
    Trainer view: basic statistics on consultation requests.
    Uses ConsultationRequest to build simple counts.
    """
    # Counts by training goal
    goal_counts_qs = (
        ConsultationRequest.objects.values("training_goal")
        .annotate(total=Count("id"))
        .order_by("training_goal")
    )
    goal_labels = dict(ConsultationRequest.TRAINING_GOAL_CHOICES)
    goal_stats = [
        {
            "code": row["training_goal"],
            "label": goal_labels.get(row["training_goal"] or "", "Not specified"),
            "total": row["total"],
        }
        for row in goal_counts_qs
    ]

    # Counts by coaching option
    option_counts_qs = (
        ConsultationRequest.objects.values("coaching_option")
        .annotate(total=Count("id"))
        .order_by("coaching_option")
    )
    option_labels = dict(ConsultationRequest.COACHING_OPTION_CHOICES)
    option_stats = [
        {
            "code": row["coaching_option"],
            "label": option_labels.get(row["coaching_option"] or "", "Not specified"),
            "total": row["total"],
        }
        for row in option_counts_qs
    ]

    total_requests = sum(item["total"] for item in goal_stats)

    context = {
        "total_requests": total_requests,
        "goal_stats": goal_stats,
        "option_stats": option_stats,
    }
    return render(request, "trainer/metrics.html", context)


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
            "phase": "Weeks 1–6",
            "clients": 5,
            "status": "Active",
            "next_action": "Review week-3 check-ins",
        },
        {
            "name": "Strength foundation (4 weeks)",
            "phase": "Weeks 1–4",
            "clients": 3,
            "status": "Planning",
            "next_action": "Assign to new consultation requests",
        },
    ]

    programme_templates = [
        {
            "name": "General strength – 3 days",
            "focus": "Full-body strength",
            "length": "8 weeks",
        },
        {
            "name": "Fat-loss circuit – 2 days",
            "focus": "Conditioning / cardio",
            "length": "6 weeks",
        },
    ]

    context = {
        "programme_blocks": programme_blocks,
        "programme_templates": programme_templates,
    }
    return render(request, "trainer/programmes.html", context)
