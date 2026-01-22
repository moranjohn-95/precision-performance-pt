# accounts/views.py
from collections import OrderedDict

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.urls import reverse_lazy
from django.shortcuts import render

from training.models import ConsultationRequest


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


@login_required(login_url="accounts:client_login")
def client_dashboard(request):
    """
    Simple client dashboard. We'll flesh this out later.
    """
    return render(request, "client/dashboard.html")


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
    Placeholder for trainer overview of client metrics.
    """
    return render(request, "trainer/metrics.html")


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
