from django import forms

from .models import Plan
from .models import Schedule
from .models import Cost, CostCategory



class PlanCreateForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["plan_name", "start_date", "end_date"]
        widgets = {
            "plan_name": forms.TextInput(
                attrs={
                    "placeholder": "旅行タイトル  入力"
                }
            ),
            "start_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"}
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
        fields = ["category","name", "amount"] 
        
    def __init__(self, *args, **kwargs):
        plan = kwargs.pop("plan", None)
        super().__init__(*args, **kwargs)

        if plan:
            self.fields["category"].queryset = CostCategory.objects.filter(plan=plan)
            
class CostCategoryForm(forms.ModelForm):
    class Meta:
        model = CostCategory
        fields = ["name"]            