from celery import shared_task, current_app

from .models import Book
from .typed_dicts import LoanedBookEventData


@shared_task(name="send_user_data")
def send_user_data(
    id: int, email: str, first_name: str, last_name: str, created: bool
) -> None:
    current_app.send_task(
        "get_user_data",
        args=(id, email, first_name, last_name, created),
    )


@shared_task(name="send_loaned_book_data")
def send_loaned_book_data(**kwargs:LoanedBookEventData) -> None:
    current_app.send_task("get_loaned_book_data", kwargs={**kwargs})


@shared_task(name="get_new_book_data")
def get_new_book_data(**kwargs) -> None:
    created = kwargs.pop("created")
    if created:
        Book.objects.create(**kwargs)


@shared_task(name="get_deleted_book_data")
def get_deleted_book_data(book_id: int) -> None:
    Book.objects.get(id=book_id).delete()
