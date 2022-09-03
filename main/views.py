from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from main.models import Activity, Event, Race, EventTeam, EventTeamAthlete
from main.forms import SubmitResultForm
from main.utils import get_athlete_for_user
from main.strava_webhook import verify_callback, handle_callback
from datetime import date, timedelta

def event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    races = Race.objects.filter(event=event).order_by('start_date', 'name')

    if event.relay:
        leg_dict = {}
        for leg in races:
            leg_results = Activity.objects.filter(race=leg, hidden_from_results=False).order_by('elapsed_time')
            leg_dict[leg.name] = leg_results

        results_dict = {}
        teams = EventTeam.objects.filter(event=event)
        for team in teams:
            team_leg_dict = {}
            athletes = EventTeamAthlete.objects.filter(event_team=team)
            for athlete in athletes:
                for leg, results in leg_dict.items():
                    for result in results:
                        if result.athlete.id == athlete.id:
                            team_leg_dict[leg] = result.elapsed_time
            team_leg_list = []
            team_leg_count = 0
            for leg in leg_dict.keys():
                if leg in team_leg_dict:
                    team_leg_list.append(team_leg_dict[leg])
                    team_leg_count += 1
                else:
                    team_leg_list.append(None)
    
            if team_leg_count == len(races):
                team_total_time = sum(team_leg_list, timedelta())
            else:
                team_total_time = None

            results_dict[team.name] = team_leg_list, team_total_time

        # Sort by total time, putting unfinished teams at the end
        sorted_results_dict = dict(sorted(results_dict.items(), key=lambda item: timedelta.max if item[1][1] is None else item[1][1]))

        template_context = {
            'event': event,
            'leg_names': leg_dict.keys(),
            'results_dict': sorted_results_dict,
        }
        return render(request, 'main/event.html', template_context)
    else:
        template_context = {
            'event': event,
            'race_list': races
        }
        return render(request, 'main/event.html', template_context)

def race_results(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    activities = Activity.objects.filter(race=race, hidden_from_results=False).order_by('elapsed_time')
    results_dict = {'Female Time': [],
                    'Male Time': [],
                    'Female Age Graded': [],
                    'Male Age Graded': [],
                    }
    processed_athlete_list = []
    for activity in activities:
        if activity.athlete not in processed_athlete_list:
            if activity.athlete.sex == 'F':
                dict_list = 'Female Time'
            else:
                dict_list = 'Male Time'
            results_dict[dict_list].append(activity)
            processed_athlete_list.append(activity.athlete)

    age_graded_activities = Activity.objects.filter(race=race, hidden_from_results=False).order_by('-age_grade')
    age_graded_processed_athlete_list = []
    for age_graded_activity in age_graded_activities:
        if age_graded_activity.athlete not in age_graded_processed_athlete_list:
            if age_graded_activity.athlete.sex == 'F':
                dict_list = 'Female Age Graded'
            else:
                dict_list = 'Male Age Graded'
            results_dict[dict_list].append(age_graded_activity)
            age_graded_processed_athlete_list.append(age_graded_activity.athlete)

    template_context = {
        'race': race,
        'results_dict': results_dict,
    }
    return render(request, 'main/race_results.html', template_context)

@login_required
def submit_result(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmitResultForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            race = data.get("race")
            start_time = data.get("start_time")
            elapsed_time = data.get("elapsed_time")

            activity = Activity(
                race=race,
                athlete=get_athlete_for_user(request.user),
                start_time=start_time,
                elapsed_time=elapsed_time,
                evidence_file=request.FILES['evidence_file'] if 'evidence_file' in request.FILES else None,
            )
            activity.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmitResultForm()
        form.fields["race"].queryset = Race.objects.filter(
            submissions_close__gte=date.today(),
            start_date__lte=date.today(),
            event__active=True
        )

    return render(request, 'main/submit_result.html', {'form': form})

def event_list(request):
    events = Event.objects.filter(active=False).order_by('name')
    template_context = {
        'event_list': events
    }
    return render(request, 'main/event_list.html', template_context)

@csrf_exempt
def strava_webhook(request):
    if request.method == 'GET':
        response = verify_callback(request)
        if response:
            return JsonResponse(response)
        else:
            return HttpResponseBadRequest("Invalid Strava Verification Token")
    elif request.method == 'POST':
        try:
            handle_callback(request)
        except AttributeError:
            return HttpResponseServerError()
        return HttpResponse(f'Strava Webhook Processed')
    else:
        return HttpResponseBadRequest("Invalid request method")


def submitting_results(request):
    return render(request, 'main/submitting_results.html')


def index(request):
    events = Event.objects.filter(active=True).order_by('name')
    template_context = {
        'event_list': events
    }
    return render(request, 'main/index.html', template_context)
