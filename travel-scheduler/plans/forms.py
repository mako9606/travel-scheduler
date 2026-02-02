from django import forms

from .models import Plan
from .models import Schedule

from datetime import date




class PlanCreateForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["plan_name", "start_date", "end_date"]
        widgets = {
            "start_date": forms.SelectDateWidget(
                years=range(date.today().year, date.today().year + 6),
                empty_label=("年", "月", "日"),
            ),
            "end_date": forms.SelectDateWidget(
                years=range(date.today().year, date.today().year + 6),
                empty_label=("年", "月", "日"),
            ),
        }
        
        
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [
            "destinations",
            "arrival_time",
            "departure_time",
        ]        