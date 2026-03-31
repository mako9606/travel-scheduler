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
            "parking_available",
            "parking_fee",
            "admission_available",
            "admission_fee",
            "latitude",
            "longitude",
            "memo",
        ]
        widgets = {
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "name": forms.TextInput(attrs={"placeholder": "目的地名　入力"}),
            "address": forms.TextInput(attrs={"placeholder": "住所　入力"}),
            "memo": forms.Textarea(attrs={"placeholder": "入力"}),
        }
        

class MapPinForm(forms.ModelForm):
    class Meta:
        model = MapPin
        fields = ["name", "latitude", "longitude"]