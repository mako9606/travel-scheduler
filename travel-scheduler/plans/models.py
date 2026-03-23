from destinations.models import Destination
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

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
    
    memo = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.plan_name
    
    
def default_expires_at():
    return timezone.now() + timedelta(days=180)    

class PlanShareMember(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="share_members"
    )
    member_name = models.CharField(max_length=100)
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expires_at)

    def __str__(self):
        return f"{self.plan.plan_name} - {self.member_name}"


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
    destination = models.ForeignKey(
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