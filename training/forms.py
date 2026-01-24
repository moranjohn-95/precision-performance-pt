# training/forms.py
from django import forms
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
    class Meta:
        model = WorkoutSession
        fields = ["date", "name", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Session name, e.g. Upper Body — Week 3 / Day 2"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "General notes: how it felt, any pains, etc.",
                }
            ),
        }
