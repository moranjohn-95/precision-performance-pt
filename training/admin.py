from django.contrib import admin
from .models import ConsultationRequest


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
