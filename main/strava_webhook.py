import json
import logging
import threading

from allauth.socialaccount.models import SocialApp, SocialAccount
from contextlib import closing
from django.contrib.sites.models import Site
from django.utils.datastructures import MultiValueDictKeyError
from stravalib.client import Client

import challenge.settings
from main.strava import update_user_strava_activities

logger = logging.getLogger()


def get_user_for_strava_id(strava_id):
    social_account = SocialAccount.objects.get(uid=strava_id)
    return social_account.user


def get_subscription(recycle=False):
    with closing(Client()) as client:
        strava_app = SocialApp.objects.get(name="Strava")
        subscriptions = client.list_subscriptions(
            client_id=strava_app.client_id, client_secret=strava_app.secret
        )
        subscription_count = 0
        for subscription in subscriptions:
            logger.info(
                f"Subscription present with url {subscription.callback_url} created at {subscription.created_at}"
            )
            if recycle:
                client.delete_subscription(
                    subscription.id,
                    client_id=strava_app.client_id,
                    client_secret=strava_app.secret,
                )
            else:
                subscription_count += 1

        if not subscription_count:
            logger.warning("There is currently no Strava webhook subscription set up")
            site_domain = Site.objects.get_current().domain
            callback_url = f"https://{site_domain}/strava/webhook/{challenge.settings.STRAVA_VERIFY_TOKEN}"
            logger.info(
                f"""Setting up webhook with
            client_id: {strava_app.client_id}
            callback_url: {callback_url}
            verify_token: {challenge.settings.STRAVA_VERIFY_TOKEN}
            """
            )
            client.create_subscription(
                client_id=strava_app.client_id,
                client_secret=strava_app.secret,
                callback_url=callback_url,
                verify_token=challenge.settings.STRAVA_VERIFY_TOKEN,
            )


def verify_callback(request):
    with closing(Client()) as client:
        try:
            strava_request = {
                k: request.GET[k]
                for k in ("hub.challenge", "hub.mode", "hub.verify_token")
            }
            logger.info("Handled valid Strava subscription callback")
            return client.handle_subscription_callback(
                strava_request, verify_token=challenge.settings.STRAVA_VERIFY_TOKEN
            )
        except (AssertionError, MultiValueDictKeyError):
            logger.warning("Handled invalid Strava subscription callback")


def handle_callback(request):
    with closing(Client()) as client:
        body = json.loads(request.body)
        update = client.handle_subscription_update(body)
        logger.info(f"Handled Strava subscription callback for {update.owner_id}")
        try:
            user = get_user_for_strava_id(strava_id=update.owner_id)
            t = threading.Thread(target=update_user_strava_activities, args=[user])
            t.start()
        except SocialAccount.DoesNotExist:
            logger.warning(f"No record of Strava user {update.owner_id}")
