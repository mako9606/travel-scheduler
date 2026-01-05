from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('plan_list/', views.plan_list, name='plan_list'),
    path('new/', views.PlanCreateView.as_view(), name='plan_create'),
    path('detail/', views.PlanDetailView.as_view(), name='plan_detail'),
    path('plan_edit/', views.plan_edit, name='plan_edit'),
]