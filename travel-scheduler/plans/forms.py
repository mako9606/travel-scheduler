from django import forms

from .models import Plan
from .models import Schedule
from .models import Cost

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
            "destination",
            "arrival_time",
            "departure_time",
        ]
        
        widgets = {
            "arrival_time": forms.TimeInput(
                format="%H:%M",
                attrs={"type": "time"}
            ),
            "departure_time": forms.TimeInput(
                format="%H:%M",
                attrs={"type": "time"}
            ),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["destination"].required = True
        self.fields["arrival_time"].required = True
        self.fields["departure_time"].required = True   
        
         
class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ["name", "amount"]         