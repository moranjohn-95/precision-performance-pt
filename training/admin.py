from django.contrib import admin
from .models import (
    ConsultationRequest,
    WorkoutSession,
    WorkoutSet,
    BodyMetricEntry,
)


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "training_goal",
        "coaching_option",
        "status",
        "assigned_trainer",
        "created_at",
    )
    list_filter = (
        "status",
        "coaching_option",
        "training_goal",
        "preferred_date",
        "assigned_trainer",
        "created_at",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ("client", "date", "name", "created_at")
    list_filter = ("date", "client")
    search_fields = ("name", "client__email", "client__username")
    ordering = ("-date", "-created_at")


@admin.register(WorkoutSet)
class WorkoutSetAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "exercise_name",
        "set_number",
        "reps",
        "weight_kg",
        "rpe",
    )
    list_filter = ("exercise_name", "session__client")
    search_fields = ("exercise_name", "session__name")


@admin.register(BodyMetricEntry)
class BodyMetricEntryAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "date",
        "bodyweight_kg",
        "waist_cm",
        "bench_top_set_kg",
        "sleep_hours",
    )
    list_filter = ("date", "client")
    search_fields = ("client__email", "client__username")
    ordering = ("-date", "-created_at")
