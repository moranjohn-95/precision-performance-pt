from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import (
    ClientProgramme,
    ProgrammeBlock,
    ProgrammeDay,
    WorkoutSession,
)


class WorkoutSessionDuplicateTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.client_user = User.objects.create_user(
            username="client", email="client@example.com", password="test"
        )
        self.trainer = User.objects.create_user(
            username="trainer", email="trainer@example.com", password="test"
        )

        self.block = ProgrammeBlock.objects.create(
            name="Block A", weeks=6
        )
        self.day = ProgrammeDay.objects.create(
            block=self.block,
            name="Day 1",
            order=1,
        )
        self.client_programme = ClientProgramme.objects.create(
            client=self.client_user,
            trainer=self.trainer,
            block=self.block,
            status="active",
        )

    def test_duplicate_week_day_not_allowed(self):
        WorkoutSession.objects.create(
            client=self.client_user,
            client_programme=self.client_programme,
            programme_day=self.day,
            week_number=1,
            name="Week 1 - Day 1",
        )

        with self.assertRaises(IntegrityError):
            WorkoutSession.objects.create(
                client=self.client_user,
                client_programme=self.client_programme,
                programme_day=self.day,
                week_number=1,
                name="Week 1 - Day 1 duplicate",
            )
