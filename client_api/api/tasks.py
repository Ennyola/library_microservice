from celery import shared_task

from .models import User


@shared_task(name="get_users")
def get_users() -> User:
    return User.objects.all()
