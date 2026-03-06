from .models import ShortcutType, UserShortcut
from django.urls import reverse

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
        

SHORTCUT_URL_MAP = {
    "plan_list": "plans:plan_list",
    #"plan_day": "plans:plan_detail",
    #"plan_map": "plans:plan_map",
    #"plan_cost": "plans:plan_cost",
    #"plan_memo": "plans:plan_memo",
    "memo": "memos:memo_list",
}


def get_shortcut_url(action_key):
    url_name = SHORTCUT_URL_MAP.get(action_key)

    if not url_name:
        return "#"

    return reverse(url_name)        