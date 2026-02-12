from django.contrib import admin
from .models import Plan, DaySchedule, Schedule, Cost, CostCategory

admin.site.register(Plan)
admin.site.register(DaySchedule)
admin.site.register(Schedule)
admin.site.register(Cost)
admin.site.register(CostCategory)