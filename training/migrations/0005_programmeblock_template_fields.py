from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0004_alter_consultationrequest_preferred_time_window_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="programmeblock",
            name="is_template",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="programmeblock",
            name="parent_template",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tailored_copies",
                to="training.programmeblock",
            ),
        ),
        migrations.AlterField(
            model_name="programmeblock",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="Trainer who created this programme template.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="programme_blocks_created",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
