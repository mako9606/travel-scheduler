from django import forms
from .models import Destination, MapPin


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            "name",
            "address",
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