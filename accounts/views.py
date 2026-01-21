# accounts/views.py
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
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


@user_passes_test(is_trainer, login_url="accounts:trainer_login")
def trainer_dashboard(request):
    """
    Trainer / owner dashboard showing recent consultation requests.
    """
    new_requests = ConsultationRequest.objects.order_by("-created_at")[:5]
    total_requests = ConsultationRequest.objects.count()

    context = {
        "new_requests": new_requests,
        "total_requests": total_requests,
    }
    return render(request, "trainer/dashboard.html", context)
