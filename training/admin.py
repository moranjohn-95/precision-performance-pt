from django.contrib import admin
from .models import (
    ConsultationRequest,
    ContactQuery,
    WorkoutSession,
    WorkoutSet,
    BodyMetricEntry,
    ProgrammeBlock,
    ProgrammeDay,
    ProgrammeExercise,
    ClientProgramme,
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


@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "topic",
        "status",
        "urgency",
        "created_at",
    )
    search_fields = ("first_name", "last_name", "email", "subject")
    list_filter = ("topic", "status", "urgency")
    ordering = ("-created_at",)


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


class ProgrammeExerciseInline(admin.TabularInline):
    model = ProgrammeExercise
    extra = 2


class ProgrammeDayInline(admin.StackedInline):
    model = ProgrammeDay
    extra = 1
    show_change_link = True


@admin.register(ProgrammeBlock)
class ProgrammeBlockAdmin(admin.ModelAdmin):
    list_display = ("name", "weeks", "created_by")
    inlines = [ProgrammeDayInline]


@admin.register(ProgrammeDay)
class ProgrammeDayAdmin(admin.ModelAdmin):
    list_display = ("name", "block", "order")
    inlines = [ProgrammeExerciseInline]
    ordering = ("block", "order")


@admin.register(ProgrammeExercise)
class ProgrammeExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "exercise_name",
        "day",
        "target_sets",
        "target_reps",
        "target_weight_kg",
        "order",
    )
    ordering = ("day", "order")


@admin.register(ClientProgramme)
class ClientProgrammeAdmin(admin.ModelAdmin):
    list_display = ("client", "trainer", "block", "status", "start_date")
    list_filter = ("status", "block")
