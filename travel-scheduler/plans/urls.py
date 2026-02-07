from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('plan_list/', views.plan_list, name='plan_list'),
    path('new/', views.PlanCreateView.as_view(), name='plan_create'),
    path('detail/<int:pk>/', views.PlanDetailView.as_view(), name='plan_detail'),
    path("reorder/", views.plan_reorder, name="plan_reorder"), #プランリスト順番入れ替え
    path('plan_edit/', views.plan_edit, name='plan_edit'),
    path('plan_delete/', views.plan_delete, name='plan_delete'),
    path('share/', views.plan_share, name='plan_share'),
    path('revoke/', views.share_revoke, name='share_revoke'),
    path("cost-edit/",views.plan_cost_edit,name="plan_cost_edit"),
    path("schedule/<int:pk>/edit/", views.schedule_edit, name="schedule_edit"), #編集時用
    path("schedule/create/", views.schedule_create, name="schedule_create"), #新規追加用
    path("schedule/reorder/", views.schedule_reorder, name="schedule_reorder"),#目的地の順番入れ替え用
    path("schedule-memo/", views.schedule_memo, name="schedule_memo"),
]