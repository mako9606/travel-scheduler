from django.contrib import admin
from .models import ShortcutType, UserShortcut

admin.site.register(ShortcutType)
admin.site.register(UserShortcut)
