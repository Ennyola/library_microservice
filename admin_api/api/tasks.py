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


@shared_task(name="send_new_book_data")
def send_new_book_data(**kwargs):
    current_app.send_task("get_new_book_data", kwargs={**kwargs})


@shared_task(name="send_deleted_book_data")
def send_deleted_book_data(book_id: int):
    current_app.send_task("get_deleted_book_data", args=(book_id,))
