# Generated by Django 4.0 on 2022-01-01 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_alter_race_route_gpx_alter_race_route_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="athlete",
            old_name="gender",
            new_name="sex",
        ),
    ]
