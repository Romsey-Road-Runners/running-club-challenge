import logging

from django.core.management.base import BaseCommand
from main.strava_webhook import get_subscription

logger = logging.getLogger()


class Command(BaseCommand):
    help = "Ensure we have a Strava subscription set up"

    def add_arguments(self, parser):
        parser.add_argument(
            "--recycle",
            action="store_true",
            help="Delete any existing Strava webhook subscriptions",
        )

    def handle(self, *args, **options):
        if options["recycle"]:
            recycle = True
        else:
            recycle = False
        get_subscription(recycle=recycle)
