"""Service helpers for consultation assignment."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.db import transaction
from django.urls import reverse

from accounts.models import ClientProfile
from training.models import ConsultationRequest

User = get_user_model()


def _build_response(ok, redirect_name, redirect_kwargs, level, message):
    """Return a small, consistent response dict."""
    return {
        "ok": ok,
        "redirect": reverse(redirect_name, kwargs=redirect_kwargs)
        if redirect_kwargs
        else reverse(redirect_name),
        "message_level": level,
        "message": message,
    }


def assign_consultation_to_trainer(*, request, consultation, trainer_user):
    """
    Move consultation to a trainer's client list.
    Behaviour mirrors the inline logic in trainer_consultation_detail.
    """
    # Block group coaching; must go to Current Classes instead.
    if consultation.coaching_option in ["small_group", "large_group"]:
        return _build_response(
            ok=False,
            redirect_name="accounts:trainer_consultation_detail",
            redirect_kwargs={"pk": consultation.pk},
            level="error",
            message=(
                "Group coaching requests must be added to Current Classes, "
                "not assigned to the client list."
            ),
        )

    # Block if already assigned to another trainer and not owner.
    already_assigned = (
        consultation.assigned_trainer
        and consultation.assigned_trainer != trainer_user
        and not trainer_user.is_superuser
    )
    if already_assigned:
        return _build_response(
            ok=False,
            redirect_name="accounts:trainer_clients",
            redirect_kwargs=None,
            level="error",
            message="This consultation is already assigned to another trainer.",
        )

    user = None
    needs_reset = False

    with transaction.atomic():
        email_val = (consultation.email or "").strip()
        first = consultation.first_name or ""
        last = consultation.last_name or ""

        # Find or create user by email.
        user = User.objects.filter(email__iexact=email_val).first()
        user_created = False
        if user is None and email_val:
            base_username = email_val.split("@")[0] or "client"
            username = base_username
            suffix = 1
            while User.objects.filter(username__iexact=username).exists():
                username = f"{base_username}{suffix}"
                suffix += 1

            user = User.objects.create(
                username=username,
                email=email_val,
                first_name=first,
                last_name=last,
            )
            user.set_unusable_password()
            user.save()
            user_created = True

        # Link or create client profile.
        if user:
            profile, _ = ClientProfile.objects.get_or_create(user=user)
            if profile.preferred_trainer is None:
                profile.preferred_trainer = trainer_user
            if profile.consultation_request is None:
                profile.consultation_request = consultation
            profile.save()
            needs_reset = user_created or (
                user and not user.has_usable_password()
            )

        consultation.assigned_trainer = trainer_user
        consultation.status = ConsultationRequest.STATUS_ASSIGNED
        consultation.save()

    # Send password reset/setup email if needed.
    if needs_reset and user and user.email:
        try:
            form = PasswordResetForm({"email": user.email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                )
            return _build_response(
                ok=True,
                redirect_name="accounts:trainer_clients",
                redirect_kwargs=None,
                level="success",
                message="Account created and password setup email sent.",
            )
        except Exception:
            return _build_response(
                ok=True,
                redirect_name="accounts:trainer_clients",
                redirect_kwargs=None,
                level="warning",
                message=(
                    "Account created. Client can set password using the "
                    "Forgot password link."
                ),
            )

    return _build_response(
        ok=True,
        redirect_name="accounts:trainer_clients",
        redirect_kwargs=None,
        level="success",
        message="Client has been added to the trainer client list.",
    )
