from django.db import models

# Create your models here.


class ConsultationRequest(models.Model):
    TRAINING_GOAL_CHOICES = [
        ("fat_loss", "Fat loss / body composition"),
        ("strength", "Strength & performance"),
        ("health", "General health & fitness"),
        ("sport", "Sport-specific training"),
        ("other", "Other / not sure yet"),
    ]

    COACHING_OPTION_CHOICES = [
        ("1to1", "1:1 Personal Training"),
        ("small_group", "Small Group Coaching"),
        ("large_group", "Larger Group Classes"),
        ("online", "Online Coaching"),
    ]

    TIME_WINDOW_CHOICES = [
        ("early_morning", "Early morning (06:00–09:00)"),
        ("late_morning", "Late morning (09:00–12:00)"),
        ("early_afternoon", "Early afternoon (12:00–15:00)"),
        ("late_afternoon", "Late afternoon (15:00–18:00)"),
        ("evening", "Evening (18:00–20:30)"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)

    training_goal = models.CharField(
        max_length=20,
        choices=TRAINING_GOAL_CHOICES,
        blank=True,
    )

    coaching_option = models.CharField(
        max_length=20,
        choices=COACHING_OPTION_CHOICES,
        blank=True,
    )

    preferred_date = models.DateField(null=True, blank=True)

    preferred_time_window = models.CharField(
        max_length=20,
        choices=TIME_WINDOW_CHOICES,
        blank=True,
    )

    availability_notes = models.TextField(blank=True)

    training_background = models.TextField(blank=True)

    contact_consent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} – {self.email}"
