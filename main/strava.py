import datetime
import logging

from allauth.socialaccount.models import SocialAccount, SocialToken
from stravalib import unithelper
from stravalib.client import Client

from .calculators import race_distance_in_km
from .models import Race
from .utils import create_update_activity, get_athlete_for_user

logger = logging.getLogger()


def get_user_strava_token(user):
    social_accounts = SocialAccount.objects.filter(user=user)
    if social_accounts:
        social_tokens = SocialToken.objects.filter(account=social_accounts[0])
        if social_tokens:
            return social_tokens[0]
    return False


def update_user_strava_token(token):
    if token.expires_at < datetime.datetime.now(tz=datetime.timezone.utc):
        client = Client()
        refresh_response = client.refresh_access_token(
            client_id=token.app.client_id,
            client_secret=token.app.secret,
            refresh_token=token.token_secret,
        )
        token.token = refresh_response["access_token"]
        token.secret = refresh_response["refresh_token"]
        token.expires_at = datetime.datetime.fromtimestamp(
            refresh_response["expires_at"], tz=datetime.timezone.utc
        )
        token.save()
        logger.info(f"Refreshed Strava token for {token.account}")
    logger.debug(f"Did not need to refresh Strava token for {token.account}")


def update_user_strava_activities(user):
    if not user.is_active:
        logger.info(
            f"Skipping Strava update for {user.first_name} {user.last_name} until their account is activated"
        )
        return
    token = get_user_strava_token(user)
    if not token:
        logger.info(f"No Strava token for user {user.first_name} {user.last_name}")
        return
    logger.debug(f"Got strava token for {user.first_name} {user.last_name}")
    update_user_strava_token(token)

    logger.info(f"Updating Strava activities for {user.first_name} {user.last_name}")
    a_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    client = Client()
    client.access_token = token.token
    client.refresh_token = token.token_secret
    client.token_expires_at = token.expires_at
    strava_activities = client.get_activities(after=a_week_ago)
    races = Race.objects.filter(
        submissions_close__gte=datetime.date.today(),
        start_date__lte=datetime.date.today(),
    )
    for strava_activity in strava_activities:
        logger.debug(
            f"Processing strava activity ({strava_activity.id}) {strava_activity.name} for {user.first_name} {user.last_name}"
        )
        logger.debug(
            f"Activity distance {strava_activity.distance}, date {strava_activity.start_date} and time {strava_activity.elapsed_time}"
        )
        if strava_activity.type == "Run" or strava_activity.type == "Walk":
            for race in races:
                if not race.match_text:
                    continue
                race_distance_km = race_distance_in_km(race)
                strava_name_sanitised = " ".join(strava_activity.name.lower().split())
                strava_distance_km = unithelper.kilometers(strava_activity.distance).num
                if (
                    race.start_date
                    <= strava_activity.start_date.date()
                    <= race.end_date
                    and race.match_text.lower() in strava_name_sanitised
                    and race_distance_km * 0.98
                    < strava_distance_km
                    < race_distance_km * 1.05
                ):
                    logger.info(
                        f"Found match for race {race.name}: {strava_activity.name} for {user.first_name} "
                        f"{user.last_name} of distance {round(strava_distance_km, 2)}km at {strava_activity.start_date} "
                        f"and time {strava_activity.elapsed_time}"
                    )
                    create_update_activity(
                        race=race,
                        athlete=get_athlete_for_user(user),
                        start_time=strava_activity.start_date,
                        elapsed_time=strava_activity.elapsed_time,
                        strava_activity_id=strava_activity.id,
                    )
