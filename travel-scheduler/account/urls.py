from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.account, name='account'),
    path('edit-email/', views.edit_email, name='edit_email'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-complete/', views.password_complete, name='password_complete'),
    path('logout/', views.logout, name='logout'),
    # ↓ログアウト処理（POST）
    path('logout/execute/', LogoutView.as_view(), name='logout_execute'),
]