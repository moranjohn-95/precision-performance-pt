# training/forms.py
from django import forms
from django.utils import timezone

from .models import ConsultationRequest, WorkoutSession


class ConsultationRequestForm(forms.ModelForm):
    """
    Handles validation for the 'Book a consultation' form.
    """

    # Ensure the browser shows a calendar widget
    preferred_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = ConsultationRequest
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "training_goal",
            "coaching_option",
            "preferred_date",
            "preferred_time_window",
            "availability_notes",
            "training_background",
            "contact_consent",
        ]

        # Django’s server-side validation and error messages.
        widgets = {
            "availability_notes": forms.Textarea(attrs={"rows": 3}),
            "training_background": forms.Textarea(attrs={"rows": 5}),
        }

        error_messages = {
            "first_name": {
                "required": "Please enter your first name.",
            },
            "last_name": {
                "required": "Please enter your last name.",
            },
            "email": {
                "required": "We need an email address to contact you.",
            },
            "coaching_option": {
                "required": (
                    "Please choose the coaching option you’re most "
                    "interested in."
                ),
            },
        }

    def clean_contact_consent(self):
        """
        Make consent explicitly required, and give a human-friendly message.
        """
        consent = self.cleaned_data.get("contact_consent")
        if not consent:
            raise forms.ValidationError(
                "Please confirm that we can contact you about your "
                "consultation request."
            )
        return consent


class WorkoutSessionForm(forms.ModelForm):
    # Extra fields for the 3 exercises × 3 sets in the UI
    bench_set1 = forms.CharField(required=False, label="Bench – Set 1")
    bench_set2 = forms.CharField(required=False, label="Bench – Set 2")
    bench_set3 = forms.CharField(required=False, label="Bench – Set 3")

    row_set1 = forms.CharField(required=False, label="Row – Set 1")
    row_set2 = forms.CharField(required=False, label="Row – Set 2")
    row_set3 = forms.CharField(required=False, label="Row – Set 3")

    incline_set1 = forms.CharField(required=False, label="DB Incline – Set 1")
    incline_set2 = forms.CharField(required=False, label="DB Incline – Set 2")
    incline_set3 = forms.CharField(required=False, label="DB Incline – Set 3")

    class Meta:
        model = WorkoutSession
        fields = ["date", "name", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Session name (e.g. Upper Body — Week 3 / Day 2)"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Any general notes about the session.",
                }
            ),
        }

    def _build_details_summary(self):
        cd = self.cleaned_data
        lines = []

        def add_line(label, s1, s2, s3):
            if s1 or s2 or s3:
                parts = [p for p in (s1, s2, s3) if p]
                lines.append(f"{label}: " + " | ".join(parts))

        add_line(
            "Bench Press",
            cd.get("bench_set1"),
            cd.get("bench_set2"),
            cd.get("bench_set3"),
        )
        add_line(
            "Seated Row",
            cd.get("row_set1"),
            cd.get("row_set2"),
            cd.get("row_set3"),
        )
        add_line(
            "DB Incline",
            cd.get("incline_set1"),
            cd.get("incline_set2"),
            cd.get("incline_set3"),
        )

        return "\n".join(lines)

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        # Default to today's date if left blank
        if not instance.date:
            instance.date = timezone.localdate()

        # Attach client if not already set
        if user is not None and getattr(instance, "client_id", None) is None:
            instance.client = user

        # Default status to "logged" if the model has a status field
        if hasattr(instance, "status") and not getattr(instance, "status", None):
            try:
                instance.status = "logged"
            except Exception:
                pass

        # Build a structured text summary of the sets into notes
        details = self._build_details_summary()
        if details:
            if instance.notes:
                instance.notes = instance.notes + "\n\nSession details:\n" + details
            else:
                instance.notes = "Session details:\n" + details

        if commit:
            instance.save()

        return instance
