from django.conf import settings
from django.db import models


class ClientProfile(models.Model):
    """
    Extra information for a coaching client.
    Linked one-to-one with the Django User model.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_profile",
    )

    # Optional link back to the consultation that started the relationship
    consultation_request = models.ForeignKey(
        "training.ConsultationRequest",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="converted_clients",
    )

    # Some basic coaching metadata (all optional for now)
    preferred_trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients_managed",
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("user__username",)

    def __str__(self):
        return f"ClientProfile for {self.user.get_username()}"
