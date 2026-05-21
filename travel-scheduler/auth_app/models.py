from django.db import models
from django.conf import settings


class HomeGuideSetting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="home_guide_setting"
    )
    hide_home_guide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} home guide"