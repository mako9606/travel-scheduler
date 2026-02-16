from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Destination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destinations")
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    url = models.CharField(max_length=225, blank=True)
    open_at = models.TimeField(null=True, blank=True)
    close_at = models.TimeField(null=True, blank=True)
    closed_day = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
