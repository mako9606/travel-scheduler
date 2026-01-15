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
     
     
     
    # 「username/email をDBに保存する前に、前後の空白を削除してください」    
    def clean_username(self):
        return self.cleaned_data["username"].strip()
    
    def clean_email(self):
        return self.cleaned_data["email"].strip()