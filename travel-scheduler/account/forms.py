from django import forms
from django.contrib.auth import get_user_model

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