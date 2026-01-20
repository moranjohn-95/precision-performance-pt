# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("trainer/login/", views.trainer_login, name="trainer_login"),
    path("client/login/", views.client_login, name="client_login"),
]
