from django.urls import path
from . import views

app_name = 'memos'

urlpatterns = [
    path('memo-list/', views.memo_list, name='memo_list'),
]