# Generated by Django 4.0 on 2021-12-15 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Race",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=254)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("distance", models.IntegerField()),
                (
                    "distance_unit",
                    models.CharField(
                        choices=[("M", "Miles"), ("K", "Kilometres")], max_length=1
                    ),
                ),
                ("strava_segment_id", models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Athlete",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("F", "Female"), ("M", "Male")],
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "DOB",
                    models.DateField(
                        blank=True, null=True, verbose_name="Date of Birth"
                    ),
                ),
                (
                    "photo",
                    models.URLField(
                        blank=True,
                        max_length=254,
                        null=True,
                        verbose_name="Profile Photo URL",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="auth.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("elapsed_time", models.DurationField()),
                ("evidence", models.URLField(blank=True, max_length=1024, null=True)),
                ("strava_activity_id", models.BigIntegerField(blank=True, null=True)),
                (
                    "athlete",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.athlete"
                    ),
                ),
                (
                    "race",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.race"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "activities",
            },
        ),
    ]
