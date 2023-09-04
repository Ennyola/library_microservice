from celery import shared_task, current_app

from .models import User


@shared_task(name="get_user_data")
def get_user_data(
    id: int, email: str, first_name: str, last_name: str, created: bool
) -> None:
    if created:
        User.objects.create(
            id=id, email=email, first_name=first_name, last_name=last_name
        )
