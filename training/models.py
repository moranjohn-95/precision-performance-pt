from django.conf import settings
from django.db import models
from django.utils import timezone


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

    STATUS_NEW = "new"
    STATUS_ASSIGNED = "assigned"
    STATUS_CONTACTED = "contacted"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_CONTACTED, "Contacted"),
        (STATUS_CLOSED, "Closed"),
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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    assigned_trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="assigned_consultations",
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.email}"


class WorkoutSession(models.Model):
    """
    One workout completed by a client on a given date.
    """

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workout_sessions",
    )
    date = models.DateField(default=timezone.now)
    name = models.CharField(
        max_length=120,
        help_text="Short label such as 'Upper Body — Week 3 / Day 2'.",
    )
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self) -> str:
        return f"{self.client} – {self.name} – {self.date}"


class WorkoutSet(models.Model):
    """
    A single set within a workout session.
    """

    session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        related_name="sets",
    )
    exercise_name = models.CharField(max_length=120)
    set_number = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Working weight in kg (if applicable).",
    )
    rpe = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RPE / effort rating for the set.",
    )

    class Meta:
        ordering = ["session", "exercise_name", "set_number"]

    def __str__(self) -> str:
        return f"{self.session} – {self.exercise_name} set {self.set_number}"


class BodyMetricEntry(models.Model):
    """
    Periodic check-in metrics for a client.
    """

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="body_metrics",
    )
    date = models.DateField(default=timezone.now)

    bodyweight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    waist_cm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    bench_top_set_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Heaviest top set for bench in kg.",
    )
    sleep_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self) -> str:
        return f"{self.client} – {self.date}"
