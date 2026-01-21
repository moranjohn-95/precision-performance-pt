# accounts/views.py
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


@login_required
@user_passes_test(lambda u: u.is_staff)
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

    context = {
        "latest_requests": latest_requests,
        "total_requests": total_requests,
        "coaching_breakdown": coaching_breakdown,
    }
    return render(request, "trainer/dashboard.html", context)
