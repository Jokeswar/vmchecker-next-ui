# Generated by Django 4.1 on 2022-09-06 20:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Assignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("gitlab_private_token", models.CharField(max_length=40)),
                ("gitlab_project_id", models.BigIntegerField()),
                ("long_name", models.CharField(max_length=256)),
                ("short_name", models.CharField(max_length=64)),
                ("description", models.TextField(blank=True, null=True)),
                ("max_score", models.DecimalField(decimal_places=2, max_digits=5)),
                ("deadline_soft", models.DateTimeField(blank=True, null=True)),
                ("deadline_hard", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("feedback", models.TextField(null=True)),
                (
                    "reviewer",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("evaluator_job_id", models.IntegerField()),
                ("score", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("assignment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="ui.assignment")),
                (
                    "feedback",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="ui.feedback"
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
