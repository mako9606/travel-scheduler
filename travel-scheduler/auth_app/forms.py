from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        try:
            user = User.objects.get(email=email)
            self.cleaned_data['username'] = user.username
        except User.DoesNotExist:
            raise forms.ValidationError("メールアドレスが存在しません")
        
        return super().clean()