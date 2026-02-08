from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('search/', views.destination_search, name='destination_search'),
    path('create/', views.destination_create, name="destination_create"),#新規追加用
    path('edit/<int:pk>/', views.destination_edit, name='destination_edit'),#編集時用
    path('delete/<int:pk>/', views.destination_delete, name='destination_delete'),
    path('detail/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('map/', views.map_destination, name="map_destination"),
    path('map/pin-edit/', views.map_pin_edit, name="map_pin_edit"),
    path('map/pin-delete/', views.map_pin_delete, name="map_pin_delete"),

]
