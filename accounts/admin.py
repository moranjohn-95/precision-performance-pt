from django.contrib import admin

from .models import ClientProfile


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "preferred_trainer",
        "consultation_request",
        "created_at",
    )
    list_filter = ("preferred_trainer", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "consultation_request__email",
        "consultation_request__last_name",
    )
    readonly_fields = ("created_at", "updated_at")
