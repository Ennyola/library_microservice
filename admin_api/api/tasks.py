from celery import shared_task, current_app

from .models import User, LoanedBook, Book


@shared_task(name="get_user_data")
def get_user_data(
    id: int, email: str, first_name: str, last_name: str, created: bool
) -> None:
    if created:
        User.objects.create(
            id=id, email=email, first_name=first_name, last_name=last_name
        )


@shared_task(name="get_loaned_book_data")
def get_loaned_book_data(**kwargs) -> None:
    book_id = kwargs.pop("book_id")
    user_id = kwargs.pop("user_id")
    book = Book.objects.get(id=book_id)

    # The book borrowed status is changed to true since it is being loaned out
    book.borrowed = True
    book.save()
    user = User.objects.get(id=user_id)
    LoanedBook.objects.create(book=book, user=user, **kwargs)


@shared_task(name="send_new_book_data")
def send_new_book_data(**kwargs) -> None:
    current_app.send_task("get_new_book_data", kwargs={**kwargs})


@shared_task(name="send_deleted_book_data")
def send_deleted_book_data(book_id: int) -> None:
    current_app.send_task("get_deleted_book_data", args=(book_id,))
