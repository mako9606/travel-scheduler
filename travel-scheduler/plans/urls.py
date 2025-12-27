from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('plan_list/', views.plan_list, name='plan_list'),
]