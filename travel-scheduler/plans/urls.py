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
    path("cost/<int:pk>/category/create/", views.cost_category_create, name="cost_category_create"),
    path("cost/<int:pk>/category/<int:category_id>/edit/", views.cost_category_edit, name="cost_category_edit"),#費用カテゴリー　編集時用
    path("cost/<int:pk>/category/<int:category_id>/delete/", views.cost_category_delete, name="cost_category_delete"),#費用カテゴリー　削除用
    path("cost/<int:pk>/edit/", views.plan_cost_edit, name="plan_cost_edit"),#費用　新規時用
    path("cost/<int:pk>/<int:cost_id>/edit/", views.plan_cost_edit, name="plan_cost_edit_item"),#費用項目　編集時用
    path("cost/<int:pk>/<int:cost_id>/delete/", views.cost_delete, name="cost_delete"),#費用項目
    path("schedule/<int:pk>/edit/", views.schedule_edit, name="schedule_edit"), #編集時用
    path("schedule/create/", views.schedule_create, name="schedule_create"), #新規追加用
    path("schedule/reorder/", views.schedule_reorder, name="schedule_reorder"),#目的地の順番入れ替え用
    path("schedule-memo/", views.schedule_memo, name="schedule_memo"),
]