from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


# ログイン時のメールアドレスログインを正常に動かすための記載↓

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username =None, password =None, **kwargs):
        print("EmailBackend呼べた:", username)   
        if username is None or password is None:
            return None
        
        
        try:
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(**{UserModel.USERNAME_FIELD: username})
            except UserModel.DoesNotExist:
                return None
          
            
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None              
        
        