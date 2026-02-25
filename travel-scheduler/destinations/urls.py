from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('search/', views.destination_search, name='destination_search'),
    path('create/', views.destination_create, name="destination_create"),#新規追加用
    path('edit/<int:pk>/', views.destination_edit, name='destination_edit'),#編集時用
    path('delete/<int:pk>/', views.destination_delete, name='destination_delete'),
    path('detail/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('map/<int:pk>/', views.map_destination, name="map_destination"),
    #path("map/<destination_id>/pin/create/", views.map_pin_create, name="map_pin_create"),
    path('map/<destination_id>/pin/edit/', views.map_pin_edit, name="map_pin_edit"), #追加時
    path('map/<int:destination_id>/pin/<int:pin_id>/edit/', views.map_pin_edit, name="map_pin_edit"), #編集時
    path('map/<int:destination_id>/pin/<int:pin_id>/delete/', views.map_pin_delete, name="map_pin_delete"),
]
