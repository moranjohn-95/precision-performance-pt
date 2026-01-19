# training/forms.py
from django import forms
from .models import ConsultationRequest


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
