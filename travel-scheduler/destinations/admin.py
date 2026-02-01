from django.contrib import admin
from .models import Destination

# デコレータ登録↓

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

