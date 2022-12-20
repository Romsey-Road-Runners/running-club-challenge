from django.contrib import admin

from .models import Athlete, Event, Race, Activity, EventTeam, EventTeamAthlete


class AthleteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "sex", "DOB", "has_photo")

    @admin.display(ordering="user__first_name")
    def user_first_name(self, obj):
        return obj.user.first_name


@admin.display(ordering="-start_time")
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("race", "athlete", "elapsed_time")


class EventTeamAdmin(admin.ModelAdmin):
    list_display = ("event_name", "name")

    def event_name(self, obj):
        return obj.event.name


@admin.display(ordering="event_team")
class EventTeamAthleteAdmin(admin.ModelAdmin):
    list_display = ("event_team", "athlete")


@admin.display(ordering="event")
class RaceAdmin(admin.ModelAdmin):
    list_display = ("event", "name")


admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Event)
admin.site.register(Race, RaceAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(EventTeam, EventTeamAdmin)
admin.site.register(EventTeamAthlete, EventTeamAthleteAdmin)
admin.site.site_header = "RRR Race Results Administration"
admin.site.site_title = "RRR Race Results Admin"
