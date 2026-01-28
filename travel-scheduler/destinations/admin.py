from django.contrib import admin
from .models import Destination, Schedule

# デコレータ登録↓

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "day",
        "destination",
        "arrival_time",
        "departure_time",
        "order",
    )
