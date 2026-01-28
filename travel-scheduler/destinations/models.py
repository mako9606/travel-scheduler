from django.db import models


class Destination(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Schedule(models.Model):
    day = models.ForeignKey(
        "plans.DaySchedule",
        on_delete=models.CASCADE,
        related_name="day_schedules"
    )
    destination = models.ForeignKey(
         "destinations.Destination",
        on_delete=models.CASCADE,
        related_name="destination_schedules"
    )

    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True)

    cost_category = models.CharField(max_length=50, blank=True)
    amount = models.IntegerField(null=True, blank=True)

    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)