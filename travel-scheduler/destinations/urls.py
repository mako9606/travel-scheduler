from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('search/', views.destination_search, name='destination_search'),
]
