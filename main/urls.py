from django.urls import path

import challenge.settings
from . import views

urlpatterns = [
    path('events', views.event_list, name='event_list'),
    path('event/<int:event_id>', views.event, name='event'),
    path('event/<int:event_id>/results', views.event_results, name='event_results'),
    path('races/<int:race_id>', views.race_results, name='race_results'),
    path('submit_result', views.submit_result, name='submit_result'),
    path(f'strava/webhook/{challenge.settings.STRAVA_VERIFY_TOKEN}', views.strava_webhook, name='strava_webhook'),
    path('submitting_results', views.submitting_results, name='submitting_results'),
    path('', views.index, name='index'),
]
