import logging
import sys

from django.core.management.base import BaseCommand
from main.models import Athlete
from main.strava import update_user_strava_activities
from stravalib.exc import RateLimitExceeded

logger = logging.getLogger()


class Command(BaseCommand):
    help = "Gets any new athlete activities from Strava"

    def handle(self, *args, **options):
        for athlete in Athlete.objects.all():
            logger.info(f"Got athlete {athlete}")
            user = athlete.user
            try:
                update_user_strava_activities(user)
            except RateLimitExceeded:
                logger.warning(
                    f"Strava rate limit exceeded. Updates will be picked up next time."
                )
                sys.exit(0)
