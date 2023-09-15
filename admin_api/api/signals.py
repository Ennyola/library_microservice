from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Book
from .serializers import BookSerializer
from .tasks import send_new_book_data, send_deleted_book_data


@receiver(post_save, sender=Book)
def send_new_book_data_event(sender, **kwargs) -> None:
    book: Book = kwargs["instance"]
    created: bool = kwargs["created"]

    # converts the book instance into a dictionary
    serialized_book = BookSerializer(book)
    send_new_book_data.apply_async(kwargs={"created": created, **serialized_book.data})


@receiver(post_delete, sender=Book)
def send_deleted_book_data_event(sender, **kwargs) -> None:
    book_id: int = kwargs["instance"].id
    send_deleted_book_data.delay(book_id)
