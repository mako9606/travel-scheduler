from django import forms
from .models import Destination


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            "name",
            "address",
            "latitude",
            "longitude",
            "open_time",
            "close_time",
            "closed_day",
            "parking_available",
            "parking_fee",
            "admission_available",
            "admission_fee",
            "url",
            "memo",
            "pin_type",
        ]
