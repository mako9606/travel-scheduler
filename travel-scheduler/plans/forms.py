from django import forms

from .models import Plan
from .models import Schedule
from .models import Cost, CostCategory



class PlanCreateForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["plan_name", "start_date", "end_date"]
        error_messages = {
            "plan_name": {
                "required": "旅行タイトルを入力してください。",
            },
        }
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
        self.fields["arrival_time"].required = True
        self.fields["departure_time"].required = True
        
        self.fields["arrival_time"].error_messages["required"] = "到着時間を選択してください"
        self.fields["departure_time"].error_messages["required"] = "出発時間を選択してください"
        
    def clean(self):
        cleaned_data = super().clean()

        arrival_time = cleaned_data.get("arrival_time")
        departure_time = cleaned_data.get("departure_time")

        if arrival_time and departure_time and departure_time < arrival_time:
            raise forms.ValidationError("出発時間は到着時間より後にしてください。")

        return cleaned_data
        
         
class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ["category","name", "amount"] 
        
    def __init__(self, *args, **kwargs):
        plan = kwargs.pop("plan", None)
        super().__init__(*args, **kwargs)
        
        self.fields["category"].error_messages["required"] = "カテゴリーを選択してください"
        self.fields["name"].error_messages["required"] = "項目名を入力してください"
        self.fields["amount"].error_messages["required"] = "金額を入力してください"

        if plan:
            self.fields["category"].queryset = CostCategory.objects.filter(plan=plan)
            
class CostCategoryForm(forms.ModelForm):
    class Meta:
        model = CostCategory
        fields = ["name"]
        error_messages = {
            "name": {
                "required": "カテゴリー名を入力してください",
            },
        }
    
    def __init__(self, *args, **kwargs):
        self.plan = kwargs.pop("plan", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        if not name:
            return name

        categories = CostCategory.objects.filter(
            plan=self.plan,
            name=name,
        )

        if self.instance and self.instance.pk:
            categories = categories.exclude(pk=self.instance.pk)

        if categories.exists():
            raise forms.ValidationError("同じ名前のカテゴリーがあります")

        return name