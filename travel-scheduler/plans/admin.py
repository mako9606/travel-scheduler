from django.contrib import admin
from .models import Plan, DaySchedule, Schedule

admin.site.register(Plan)
admin.site.register(DaySchedule)
admin.site.register(Schedule)