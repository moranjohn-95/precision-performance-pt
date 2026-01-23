# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    TrainerLoginView,
    ClientLoginView,
    trainer_dashboard,
    trainer_clients,
    trainer_programmes,
    trainer_metrics,
    client_dashboard,
    client_programme_library,
    client_today,
    client_workout_log,
)

app_name = "accounts"

urlpatterns = [
    # Logins
    path("trainer/login/", TrainerLoginView.as_view(), name="trainer_login"),
    path("client/login/", ClientLoginView.as_view(), name="client_login"),

    # Dashboards
    path("trainer/dashboard/", trainer_dashboard, name="trainer_dashboard"),
    path("trainer/clients/", trainer_clients, name="trainer_clients"),
    path("trainer/programmes/", trainer_programmes, name="trainer_programmes"),
    path("trainer/metrics/", trainer_metrics, name="trainer_metrics"),
    path("client/dashboard/", client_dashboard, name="client_dashboard"),
    path("client/today/", client_today, name="client_today"),
    path("client/programmes/", client_programme_library, name="client_programmes"),
    path("client/workout-log/", client_workout_log, name="client_workout_log"),

    # Logout (back to home page)
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]
