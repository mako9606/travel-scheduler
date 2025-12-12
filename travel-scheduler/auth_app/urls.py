from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . forms import EmailAuthenticationForm

app_name='auth_app'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='auth_app/login.html',
            authentication_form=EmailAuthenticationForm
        ),
        name='login'
    ),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
]
