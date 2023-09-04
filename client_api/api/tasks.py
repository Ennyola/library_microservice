from celery import shared_task, current_app

from .models import User


@shared_task(name="send_user_data")
def send_user_data(
    id: int, email: str, first_name: str, last_name: str, created: bool
) -> None:
    current_app.send_task(
        "get_user_data",
        args=(id, email, first_name, last_name, created),
    )
