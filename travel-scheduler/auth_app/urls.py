from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . forms import EmailAuthenticationForm

app_name='auth_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
]
