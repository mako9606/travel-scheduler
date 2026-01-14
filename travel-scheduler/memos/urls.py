from django.urls import path
from . import views

app_name = 'memos'

urlpatterns = [
    path('list/', views.memo_list, name='memo_list'),
    path('detail/', views.memo_detail, name='memo_detail'),
    path('edit/', views.memo_edit, name='memo_edit'),
    path('delete/', views.memo_delete, name='memo_delete'),
]