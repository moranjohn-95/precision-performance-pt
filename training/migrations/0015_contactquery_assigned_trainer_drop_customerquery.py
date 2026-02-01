"""Add assigned_trainer to ContactQuery and drop CustomerQuery."""

from django.conf import settings
from django.db import migrations, models
from django.utils import timezone


def copy_customer_queries(apps, schema_editor):
    """
    Move legacy CustomerQuery rows into ContactQuery before dropping the table.
    """

    ContactQuery = apps.get_model("training", "ContactQuery")
    CustomerQuery = apps.get_model("training", "CustomerQuery")

    # Work out safe defaults from historical ContactQuery choices.
    status_field = ContactQuery._meta.get_field("status")
    valid_statuses = {c[0] for c in (status_field.choices or [])}
    default_status = "new"
    if not valid_statuses:
        default_status = "new"
    elif "new" in valid_statuses:
        default_status = "new"
    else:
        default_status = next(iter(valid_statuses))

    coaching_field = ContactQuery._meta.get_field("coaching_option")
    coaching_choices = [c[0] for c in (coaching_field.choices or [])]
    default_coaching = coaching_choices[0] if coaching_choices else "other"

    contact_field = ContactQuery._meta.get_field("preferred_contact_method")
    contact_choices = [c[0] for c in (contact_field.choices or [])]
    default_contact_method = (
        contact_choices[0] if contact_choices else "email"
    )

    for legacy in CustomerQuery.objects.all():
        full_name = legacy.full_name or ""
        parts = full_name.strip().split(" ", 1)
        first = parts[0] if parts else ""
        last = parts[1] if len(parts) > 1 else ""

        # Map old status strings into valid ContactQuery statuses.
        if legacy.status == "open" and "new" in valid_statuses:
            mapped_status = "new"
        elif legacy.status == "in_progress" and "in_progress" in valid_statuses:
            mapped_status = "in_progress"
        elif legacy.status == "closed" and "closed" in valid_statuses:
            mapped_status = "closed"
        else:
            mapped_status = default_status

        ContactQuery.objects.create(
            first_name=first or "Contact",
            last_name=last,
            email=legacy.email,
            phone="",
            coaching_option=default_coaching,
            message=f"{legacy.subject}\n\n{legacy.message}",
            preferred_contact_method=default_contact_method,
            contact_consent=False,
            assigned_trainer=legacy.assigned_trainer,
            status=mapped_status,
            created_at=legacy.created_at or timezone.now(),
            updated_at=legacy.updated_at or timezone.now(),
        )


def noop_reverse(apps, schema_editor):
    """No reverse copy; CustomerQuery table will be recreated on rollback."""
    return None


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0014_customerquery"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactquery",
            name="assigned_trainer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="assigned_contact_queries",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(copy_customer_queries, noop_reverse),
        migrations.DeleteModel(
            name="CustomerQuery",
        ),
    ]
