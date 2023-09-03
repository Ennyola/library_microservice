from celery import shared_task

from .models import User


@shared_task(name="get_users")
def get_users() -> User:
    users = User.objects.all()  # Fetch all users
    user_data = []
    for user in users:
        user_data.append(
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
    return user_data
