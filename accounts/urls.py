# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    TrainerLoginView,
    ClientLoginView,
    trainer_dashboard,
    client_dashboard,
)

app_name = "accounts"

urlpatterns = [
    # Logins
    path("trainer/login/", TrainerLoginView.as_view(), name="trainer_login"),
    path("client/login/", ClientLoginView.as_view(), name="client_login"),

    # Dashboards
    path("trainer/dashboard/", trainer_dashboard, name="trainer_dashboard"),
    path("client/dashboard/", client_dashboard, name="client_dashboard"),

    # Logout (back to home page)
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]
