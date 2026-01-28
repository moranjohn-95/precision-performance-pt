from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0007_alter_consultationrequest_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="workoutsession",
            name="client_programme",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="workout_sessions",
                to="training.clientprogramme",
            ),
        ),
        migrations.AddField(
            model_name="workoutsession",
            name="programme_day",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="workout_sessions",
                to="training.programmeday",
            ),
        ),
        migrations.AddField(
            model_name="workoutsession",
            name="week_number",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddConstraint(
            model_name="workoutsession",
            constraint=models.UniqueConstraint(
                fields=[
                    "client_programme",
                    "programme_day",
                    "week_number",
                ],
                name="uniq_session_per_week_day",
            ),
        ),
    ]
