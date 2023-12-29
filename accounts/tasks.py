# your_app/tasks.py

from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

@shared_task
def disable_inactive_users():
    # Get users who haven't logged in for 30 days
    inactive_users = User.objects.filter(
        last_login__lt=timezone.now() - timedelta(days=30)
    )

    # Disable the inactive users
    for user in inactive_users:
        user.is_active = False
        user.save()
