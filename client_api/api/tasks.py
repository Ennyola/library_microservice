from celery import shared_task, current_app

from .models import Book
from .typed_dicts import LoanedBookEventData


@shared_task(name="send_user_data")
def send_user_data(
    id: int, email: str, first_name: str, last_name: str, created: bool
) -> None:
    """
    Send a task to process user data.

    Args:
        id (int): The User's ID.
        email (str): The User's email.
        first_name (str): The User's first name.
        last_name (str): The User's last name.
        created (bool): Indicates whether the User was created.

    Returns:
        None
    """
    current_app.send_task(
        "get_user_data",
        args=(id, email, first_name, last_name, created),
    )


@shared_task(name="send_loaned_book_data")
def send_loaned_book_data(**kwargs: LoanedBookEventData) -> None:
    """
    Send a task to process loaned book data.

    Args:
        **kwargs: Keyword arguments containing data for processing.

    Returns:
        None
    """
    current_app.send_task("get_loaned_book_data", kwargs={**kwargs})


@shared_task(name="get_new_book_data")
def get_new_book_data(**kwargs) -> None:
    """
    Create a new Book object if 'created' is True.

    Args:
        **kwargs: Keyword arguments containing data for Book creation.
            Expected keys: 'id', 'title', 'author', 'publisher', 'category', 'borrowed'.

    Returns:
        None
    """
    created = kwargs.pop("created")
    if created:
        Book.objects.create(**kwargs)


@shared_task(name="get_deleted_book_data")
def get_deleted_book_data(book_id: int) -> None:
    """
    Delete a Book object by its ID.

    Args:
        book_id (int): The ID of the book to be deleted.

    Returns:
        None
    """
    Book.objects.get(id=book_id).delete()
