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
    pin_type = models.ForeignKey(
        "PinType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="destinations"
    )
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class MapPin(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="pins"
    )
    name = models.CharField(max_length=50)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.destination.name} - {self.name}"    
    
    
class PinType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type_name = models.CharField(max_length=50)
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_name
