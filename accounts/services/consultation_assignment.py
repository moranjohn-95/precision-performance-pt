"""Service helpers for consultation assignment."""

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


def _send_invite_email(request, user):
    """Send a set-password invite email; return True on success."""
    if not user or not user.email:
        return False

    try:
        form = PasswordResetForm({"email": user.email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                subject_template_name="emails/client_invite_subject.txt",
                email_template_name="emails/client_invite.txt",
                extra_email_context={"first_name": user.first_name or ""},
            )
            return True
    except Exception:
        return False
    return False


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
    user_created = False
    invite_needed = False

    with transaction.atomic():
        email_val = (consultation.email or "").strip().lower()
        first = consultation.first_name or ""
        last = consultation.last_name or ""

        # Find or create user by email.
        user = User.objects.filter(email__iexact=email_val).first()
        if user is None and email_val:
            # Use email as username so clients sign in with the email they provided.
            username = email_val
            user = User.objects.create(
                username=username,
                email=email_val,
                first_name=first,
                last_name=last,
                is_active=True,  # ensure the portal account can log in
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
            invite_needed = user_created or (
                user and not user.has_usable_password()
            )

        consultation.assigned_trainer = trainer_user
        consultation.status = ConsultationRequest.STATUS_ASSIGNED
        consultation.save()

    if invite_needed:
        sent = _send_invite_email(request, user)
        if sent:
            return _build_response(
                ok=True,
                redirect_name="accounts:trainer_clients",
                redirect_kwargs=None,
                level="success",
                message="Account created and invite email sent.",
            )
        return _build_response(
            ok=True,
            redirect_name="accounts:trainer_clients",
            redirect_kwargs=None,
            level="warning",
            message=(
                "Account created. Client can set a password using the "
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
