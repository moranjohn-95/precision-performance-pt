from django.core.management.base import BaseCommand

from training.models import ConsultationRequest


class Command(BaseCommand):
    help = (
        "Set status=ASSIGNED on 1:1/Online consultations that already have "
        "an assigned trainer but are still marked NEW."
    )

    def handle(self, *args, **options):
        qs = ConsultationRequest.objects.filter(
            assigned_trainer__isnull=False,
            status=ConsultationRequest.STATUS_NEW,
            coaching_option__in=["1to1", "online"],
        )
        updated = qs.update(status=ConsultationRequest.STATUS_ASSIGNED)
        self.stdout.write(
            self.style.SUCCESS(f"Updated {updated} consultation(s).")
        )
