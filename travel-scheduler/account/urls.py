from django.urls import path
from . import views


urlpatterns = [
    path('', views.account, name='account'),
    path('edit-email/', views.edit_email, name='edit_email'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.logout, name='logout'),
]