from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "email"]
        labels = {
            "first_name" : "アカウント名",
            "email" : "メールアドレス",
        }
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and not self.instance.first_name:
            self.fields["first_name"].initial = self.instance.username

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()

        if not first_name:
            raise forms.ValidationError("アカウント名を入力してください。")

        return first_name

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if not email:
            raise forms.ValidationError("メールアドレスを入力してください。")

        email_exists = (
            User.objects
            .exclude(pk=self.instance.pk)
            .filter(email__iexact=email)
            .exists()
        )

        username_exists = (
            User.objects
            .exclude(pk=self.instance.pk)
            .filter(username__iexact=email)
            .exists()
        )

        if email_exists or username_exists:
            raise forms.ValidationError("このメールアドレスはすでに使用されています。")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email

        if commit:
            user.save()

        return user
    
    
class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(required=False)
    new_password2 = forms.CharField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data

        new_password1 = cleaned_data.get("new_password1", "")
        new_password2 = cleaned_data.get("new_password2", "")

        # 新しいパスワードチェック
        if not new_password1:
            self.add_error("new_password1", "新しいパスワードを入力してください。")
        elif not new_password1.isascii() or not new_password1.isalnum():
            self.add_error("new_password1", "パスワードは半角英数字で入力してください。")
        else:
            try:
                validate_password(new_password1, self.user)
            except ValidationError as e:
                for message in e.messages:
                    self.add_error("new_password1", message)

        # 確認用パスワードチェック
        if not new_password2:
            self.add_error("new_password2", "新しいパスワードを再入力してください。")
        elif new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "確認用パスワードが一致しません。")

        return cleaned_data    