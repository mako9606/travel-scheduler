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
            "memo",
        ]
        widgets = {
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }