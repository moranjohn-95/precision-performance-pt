from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ConsultationRequestForm


# Create views here.
def consultation(request):
    """
    Handles the 'Book a consultation' page.

    - GET  -> show an empty form
    - POST -> validate and save the consultation request
    """

    if request.method == "POST":
        form = ConsultationRequestForm(request.POST)

        if form.is_valid():
            form.save()  # creates a ConsultationRequest in the DB

            messages.success(
                request,
                "Thank you - your consultation request has been received. "
                "A coach will get back to you shortly.",
            )

            # PRG pattern to avoid form re-submissions.
            return redirect("consultation_request")

        else:
            messages.error(
                request,
                "Please fix the errors highlighted below "
                "and submit the form again.",
            )
    else:
        form = ConsultationRequestForm()

    return render(
        request,
        "training/consultation.html",
        {"form": form},
    )
