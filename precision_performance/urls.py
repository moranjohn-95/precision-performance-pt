"""
URL configuration for precision_performance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView
from training import views as training_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home page
    path(
        "",
        TemplateView.as_view(template_name="index.html"),
        name="home",
    ),

    # Owner dashboard
    path(
        "owner/dashboard/",
        TemplateView.as_view(template_name="owner/dashboard.html"),
        name="owner-dashboard",
    ),

    # Trainer dashboard
    path(
        "trainer/dashboard/",
        TemplateView.as_view(template_name="trainer/dashboard.html"),
        name="trainer-dashboard",
    ),

    # Client dashboard
    path(
        "client/dashboard/",
        TemplateView.as_view(template_name="client/dashboard.html"),
        name="client-dashboard",
    ),

    # Booking / consultation
    path(
        "consultation/",
        training_views.consultation,
        name="consultation_request",
    ),

    # Accounts (login routes)
    path("accounts/", include("accounts.urls", namespace="accounts")),

    # Password reset flow (uses Django's built-in views/templates)
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/password-reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
