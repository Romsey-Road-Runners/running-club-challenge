import logging

from django.core.management.base import BaseCommand
from main.strava_webhook import get_subscription

logger = logging.getLogger()


class Command(BaseCommand):
    help = "Ensure we have a Strava subscription set up"

    def handle(self, *args, **options):
        get_subscription()
