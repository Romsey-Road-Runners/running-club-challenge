import logging
import uuid

import requests
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.base import ContentFile

from main.models import Athlete, Activity

logger = logging.getLogger()


def create_update_athlete(user, sex=None, dob=None, photo_url=None):
    try:
        athlete = Athlete.objects.get(user=user)
    except ObjectDoesNotExist:
        athlete = Athlete(user=user)
    except MultipleObjectsReturned:
        logger.warning("User {user.pk} has multiple associated Athletes")

    athlete.user = user
    if sex:
        athlete.sex = sex

    if dob:
        athlete.DOB = dob

    if photo_url:
        copy_athlete_photo(athlete, photo_url)

    athlete.save()


def copy_athlete_photo(athlete, photo_url):
    photo_response = requests.get(photo_url, allow_redirects=True)
    photo_extension = photo_url.split(".")[-1]
    return athlete.photo.save(
        f"{uuid.uuid4()}.{photo_extension}", ContentFile(photo_response.content)
    )


def create_update_activity(race, athlete, start_time, elapsed_time, strava_activity_id):
    existing_activities = Activity.objects.filter(
        race=race, athlete=athlete, strava_activity_id=strava_activity_id
    )
    for existing_activity in existing_activities:
        if (
            existing_activity.start_time != start_time
            or existing_activity.elapsed_time != elapsed_time
        ):
            existing_activity.start_time = start_time
            existing_activity.elapsed_time = elapsed_time
            existing_activity.save()
            logger.info(f"Updating {existing_activity.id} with new times")
        else:
            logger.info(
                f"Matching activity {existing_activity.id} doesn't need updating"
            )
        return

    # If no existing activities are returned then this will run
    logger.info(f"Creating new activity")
    activity = Activity(
        race=race,
        athlete=athlete,
        start_time=start_time,
        elapsed_time=elapsed_time,
        strava_activity_id=strava_activity_id,
    )
    activity.save()


def get_athlete_for_user(user):
    return Athlete.objects.get(user=user)
