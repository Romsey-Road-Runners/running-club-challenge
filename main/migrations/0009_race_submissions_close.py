# Generated by Django 4.0 on 2021-12-19 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_activity_hidden_from_results_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="race",
            name="submissions_close",
            field=models.DateField(default="2021-12-12"),
            preserve_default=False,
        ),
    ]
