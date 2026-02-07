from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ConsultationRequestForm, ContactQueryForm


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


def contact_us(request):
    """
    Handles the 'Contact us' page.

    - GET  -> empty ContactQueryForm
    - POST -> validate and save, then redirect (PRG)
    """
    if request.method == "POST":
        form = ContactQueryForm(request.POST)
        if form.is_valid():
            # Store the contact so owners/trainers can follow up later.
            form.save()

            messages.success(
                request,
                (
                    "Thanks - your message has been sent. A coach will get "
                    "back to you shortly."
                ),
            )
            return redirect("contact_us")
        messages.error(
            request,
            "Please fix the errors below and submit again.",
        )
    else:
        form = ContactQueryForm()

    return render(request, "training/contact.html", {"form": form})
