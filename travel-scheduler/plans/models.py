from destinations.models import Destination
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Plan(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="plans"
    )
    plan_name = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.plan_name



class DaySchedule(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="days"
    )
    date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    memo = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.plan.plan_name} - {self.date}"
    

class Schedule(models.Model):
    day = models.ForeignKey(
        DaySchedule,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    destinations = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    memo = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)


class CostCategory(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="cost_categories"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
    
class Cost(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="costs"
    )
    category = models.ForeignKey(
        CostCategory,
        on_delete=models.CASCADE,
        related_name="items"
    )    
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)