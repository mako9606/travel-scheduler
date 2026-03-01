from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import create_default_shortcuts


@receiver(user_logged_in)
def create_user_shortcuts(sender, request, user, **kwargs):
    create_default_shortcuts(user)