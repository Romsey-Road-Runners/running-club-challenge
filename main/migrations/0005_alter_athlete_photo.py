# Generated by Django 4.0 on 2021-12-18 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_remove_activity_evidence_activity_evidence_file_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="athlete",
            name="photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="Profile Photo"
            ),
        ),
    ]
