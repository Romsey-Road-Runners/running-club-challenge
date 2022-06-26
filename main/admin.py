from django.contrib import admin

from .models import Athlete, Race, Activity


class AthleteAdmin(admin.ModelAdmin):
    list_display = ("user", "sex", "DOB", "has_photo")


admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Race)
admin.site.register(Activity)
admin.site.site_header = "RRR Challenge administration"
admin.site.site_title = "RRR Challenge admin"
