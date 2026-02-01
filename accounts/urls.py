# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    TrainerLoginView,
    ClientLoginView,
    owner_queries,
    owner_query_detail,
    trainer_dashboard,
    trainer_clients,
    trainer_programmes,
    trainer_programme_detail,
    trainer_metrics,
    trainer_consultation_detail,
    trainer_client_detail,
    trainer_session_edit,
    add_to_current_classes,
    owner_dashboard,
    client_dashboard,
    client_programme_library,
    client_today,
    client_workout_log,
    client_workout_edit,
    client_metrics,
    client_support,
    client_support_tickets,
    client_support_ticket_detail,
    trainer_support,
    trainer_support_ticket,
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
    path(
        "trainer/consultations/<int:pk>/",
        trainer_consultation_detail,
        name="trainer_consultation_detail",
    ),
    path(
        "trainer/consultations/<int:pk>/add-to-classes/",
        add_to_current_classes,
        name="trainer_add_to_current_classes",
    ),
    path(
        "trainer/programmes/<int:block_id>/",
        trainer_programme_detail,
        name="trainer_programme_detail",
    ),
    path(
        "trainer/clients/<int:client_id>/",
        trainer_client_detail,
        name="trainer_client_detail",
    ),
    path(
        "trainer/sessions/<int:session_id>/edit/",
        trainer_session_edit,
        name="trainer_session_edit",
    ),
    path("owner/dashboard/", owner_dashboard, name="owner_dashboard"),
    path("owner/queries/", owner_queries, name="owner_queries"),
    path(
        "owner/queries/<int:pk>/",
        owner_query_detail,
        name="owner_query_detail",
    ),
    path("client/dashboard/", client_dashboard, name="client_dashboard"),
    path("client/today/", client_today, name="client_today"),
    # Keep legacy name/path for programme library
    path("client/programmes/", client_programme_library, name="client_programmes"),
    path(
        "client/programme-library/",
        client_programme_library,
        name="client_programme_library",
    ),
    path("client/workout-log/", client_workout_log, name="client_workout_log"),
    path(
        "client/workout-log/edit/",
        client_workout_edit,
        name="client_workout_edit",
    ),
    path("client/metrics/", client_metrics, name="client_metrics"),
    path("client/support/", client_support, name="client_support"),
    path(
        "client/support/tickets/",
        client_support_tickets,
        name="client_support_tickets",
    ),
    path(
        "client/support/tickets/<int:ticket_id>/",
        client_support_ticket_detail,
        name="client_support_ticket_detail",
    ),
    path("trainer/support/", trainer_support, name="trainer_support"),
    path(
        "trainer/support/<int:ticket_id>/",
        trainer_support_ticket,
        name="trainer_support_ticket",
    ),

    # Logout (back to home page)
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]
