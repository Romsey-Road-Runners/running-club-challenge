import logging

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from main.calculators import get_activity_age_grade

logger = logging.getLogger()


class Athlete(models.Model):
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Based on Strava API definition not mine
    # https://developers.strava.com/docs/reference/#api-models-SummaryAthlete
    SEX_CHOICES = [
        ("F", "Female"),
        ("M", "Male"),
    ]
    sex = models.CharField(
        max_length=1, choices=SEX_CHOICES, blank=True, null=True
    )
    dob = models.DateField(
        name="DOB", verbose_name="Date of Birth", blank=True, null=True
    )
    photo = models.ImageField(
        verbose_name="Profile Photo", upload_to="profile", blank=True, null=True
    )

    @admin.display(boolean=True, description="Photo")
    def has_photo(self):
        if self.photo:
            return True
        return False


class Event(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=254)
    show_total_distance = models.BooleanField(default=False)
    route_gpx = models.FileField(upload_to='route-gpx', blank=True, null=True)
    route_image = models.FileField(upload_to='route-image', blank=True, null=True)

class Race(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=254)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    submissions_close = models.DateField()
    DISTANCE_UNIT_CHOICES = [
        ("M", "Miles"),
        ("K", "Kilometres"),
    ]
    match_text = models.CharField(max_length=254)
    distance_unit = models.CharField(max_length=1, choices=DISTANCE_UNIT_CHOICES)
    route_gpx = models.FileField(upload_to='route-gpx', blank=True, null=True)
    route_image = models.FileField(upload_to='route-image', blank=True, null=True)
    strava_segment_id = models.BigIntegerField(blank=True, null=True)


class Activity(models.Model):
    def __str__(self):
        return f"{self.race.name} - {self.athlete.user.first_name} {self.athlete.user.last_name} - {self.elapsed_time}"

    class Meta:
        verbose_name_plural = "activities"

    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="Start Time (DD/MM/YYYY HH:MM)")
    elapsed_time = models.DurationField(verbose_name="Elapsed Time (MM:SS) or (HH:MM:SS)")
    age_grade = models.FloatField(editable=False)
    evidence_file = models.FileField(upload_to='evidence', blank=True, null=True)
    strava_activity_id = models.BigIntegerField(blank=True, null=True)
    hidden_from_results = models.BooleanField(default=False)


@receiver(pre_save, sender=Activity)
def calculate_age_grading(sender, instance, *args, **kwargs):
    instance.age_grade = get_activity_age_grade(instance.athlete, instance.elapsed_time, instance.race, instance.start_time)
