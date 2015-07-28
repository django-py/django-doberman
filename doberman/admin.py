from django.contrib import admin
from models import *


class FailedAccessAttemptAdmin(admin.ModelAdmin):
    """
    Failed Access Attempt Admin
    """
    list_display = (
        'modified',
        'is_locked',
        'is_expired',
        'username',
        'ip_address',
        'failed_attempts',
        'captcha_enabled',
        'captcha_passed',
        'captcha_attempts',
        'user_agent'
    )
    search_fields = ['username']

admin.site.register(FailedAccessAttempt, FailedAccessAttemptAdmin)