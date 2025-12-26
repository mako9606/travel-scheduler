from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views


urlpatterns = [
   path('', views.account, name='account'),
   path('edit-email/', views.edit_email, name='edit_email'),
   path('change-password/', views.change_password, name='change_password'),
   path('logout/', views.logout, name='logout'),
   # ↓ログアウト処理
   path('logout/execute/', LogoutView.as_view(), name='logout_execute'),
   # ↓ログイン中のパスワード変更画面
   path('password-complete/', views.password_complete, name='password_complete'),
    
   # ↓パスワード再設定メール送信
   path('password_reset/',
         auth_views.PasswordResetView.as_view(
            template_name="account/password_reset.html",
            email_template_name='account/password_reset_email.html',
            success_url=reverse_lazy('account:password_reset_done'),
         ),
         name='password_reset'),
    
   #　↓メール送信画面
   path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html"
         ),
         name='password_reset_done'),
    
   #　↓パスワード再設定画面
   path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html",
            success_url=reverse_lazy('account:password_reset_complete'),
         ),
         name='password_reset_confirm'),
    
    
   # ↓パスワード再設定完了画面
   path('password_reset_complete/',
          auth_views.PasswordResetCompleteView.as_view(
           template_name="account/password_complete.html"
          ),
          name='password_reset_complete'),
]