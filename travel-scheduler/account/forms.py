from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username" : "アカウント名",
            "email" : "メールアドレス",
        }