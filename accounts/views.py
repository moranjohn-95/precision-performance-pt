# accounts/views.py
from django.shortcuts import render


def trainer_login(request):
    """
    Placeholder trainer login page for now.
    """
    return render(request, "accounts/trainer_login.html")


def client_login(request):
    """
    Placeholder client login page for now.
    """
    return render(request, "accounts/client_login.html")
