# Generated by Django 4.1 on 2022-08-20 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0017_event_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="relay",
            field=models.BooleanField(default=False),
        ),
    ]
