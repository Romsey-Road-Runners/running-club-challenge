from django.contrib import admin

from .models import Athlete, Event, Race, Activity, EventTeam, EventTeamAthlete


class AthleteAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'DOB', 'has_photo')


admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Event)
admin.site.register(Race)
admin.site.register(Activity)
admin.site.register(EventTeam)
admin.site.register(EventTeamAthlete)
admin.site.site_header = "RRR Race Results Administration"
admin.site.site_title = "RRR Race Results Admin"
