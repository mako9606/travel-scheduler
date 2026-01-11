from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('search/', views.destination_search, name='destination_search'),
    path('edit/', views.destination_edit, name='destination_edit'),
    path('delete/', views.destination_delete, name='destination_delete'),
]
