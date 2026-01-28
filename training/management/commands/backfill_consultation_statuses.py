from django.core.management.base import BaseCommand

from training.models import ConsultationRequest


class Command(BaseCommand):
    help = (
        "Set status=ASSIGNED on 1:1/Online consultations that already have "
        "an assigned trainer but are still marked NEW. "
        "Safe to run multiple times."
    )

    def handle(self, *args, **options):
        assigned_qs = ConsultationRequest.objects.filter(
            assigned_trainer__isnull=False,
            status=ConsultationRequest.STATUS_NEW,
            coaching_option__in=["1to1", "online"],
        )
        updated_assigned = assigned_qs.update(
            status=ConsultationRequest.STATUS_ASSIGNED
        )

        classes_qs = ConsultationRequest.objects.filter(
            assigned_trainer__isnull=False,
            status=ConsultationRequest.STATUS_NEW,
            coaching_option__in=["small_group", "large_group"],
        )
        updated_classes = classes_qs.update(
            status=ConsultationRequest.STATUS_ADDED_CLASSES
        )

        total_updated = updated_assigned + updated_classes
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {total_updated} consultation(s) "
                f"({updated_assigned} assigned, {updated_classes} classes)."
            )
        )
