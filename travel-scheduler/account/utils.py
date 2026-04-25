from .models import ShortcutType, UserShortcut
from django.urls import reverse
from urllib.parse import urlencode

#ユーザー初回ログイン時にデフォルトショートカットを作成
def create_default_shortcuts(user):
    
     # すでに作成済みなら何もしない
    if UserShortcut.objects.filter(user=user).exists():
        return

    memo_type = ShortcutType.objects.get(action_key="memo")

    # 左 = メモ
    UserShortcut.objects.create(
        user=user,
        shortcut_type=memo_type,
        position=1,
    )
        
def remember_last_plan_state(user, plan_id, day_schedule_id=None, cost_id=None):
    UserShortcut.objects.filter(
        user=user,
        shortcut_type__action_key__in=[
            "plan_day",
            "plan_memo",
            "plan_map",
            "plan_cost",
        ],
    ).update(
        plan_id=plan_id,
        day_schedule_id=day_schedule_id,
        cost_id=cost_id,
    )


def get_shortcut_url(shortcut):
    action_key = shortcut.shortcut_type.action_key

    if action_key == "memo":
        return reverse("memos:memo_list")

    if action_key == "plan_list":
        return reverse("plans:plan_list")

    if action_key in ["plan_day", "plan_memo", "plan_map", "plan_cost"]:
        if not shortcut.plan_id:
            return None

        base_url = reverse("plans:plan_detail", args=[shortcut.plan_id])
        query = {}

        if shortcut.day_schedule_id:
            query["day_schedule_id"] = shortcut.day_schedule_id

        if action_key == "plan_memo":
            query["memo_tab"] = 1
        elif action_key == "plan_map":
            query["map_tab"] = 1
        elif action_key == "plan_cost":
            query["cost_tab"] = 1

        if query:
            return f"{base_url}?{urlencode(query)}"
        return base_url

    return None