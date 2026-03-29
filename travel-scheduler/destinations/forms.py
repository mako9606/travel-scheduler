from django import forms
from .models import Destination, MapPin


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            "name",
            "address",
            "url",
            "open_at",
            "close_at",
            "closed_day",   
            "latitude",
            "longitude",
            "memo",
        ]
        widgets = {
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }
        

class MapPinForm(forms.ModelForm):
    class Meta:
        model = MapPin
        fields = ["name", "latitude", "longitude"]