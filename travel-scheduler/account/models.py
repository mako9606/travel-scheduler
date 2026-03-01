from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ShortcutType(models.Model):
    display_name = models.CharField(max_length=50)
    action_key = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name



class UserShortcut(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_shortcuts"
    )

    shortcut_type = models.ForeignKey(
        ShortcutType,
        on_delete=models.CASCADE,
        related_name="shortcuts"
    )

    # 表示位置（1=左, 2=右）
    position = models.PositiveIntegerField()

    # 現在状態キャッシュ
    plan_id = models.IntegerField(null=True, blank=True)
    day_schedule_id = models.IntegerField(null=True, blank=True)
    cost_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.shortcut_type} ({self.position})"