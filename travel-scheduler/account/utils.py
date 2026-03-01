from .models import ShortcutType, UserShortcut


#ユーザー初回ログイン時にデフォルトショートカットを作成
def create_default_shortcuts(user):
    
     # すでに作成済みなら何もしない
    if UserShortcut.objects.filter(user=user).exists():
        return

    shortcut_order = [
        "plan_list",
        "plan_day",
        "plan_map",
        "plan_cost",
        "plan_memo",
        "memo",
    ]

    for index, action_key in enumerate(shortcut_order, start=1):
        shortcut_type = ShortcutType.objects.get(
            action_key=action_key
        )

        UserShortcut.objects.create(
            user=user,
            shortcut_type=shortcut_type,
            position=index,
        )