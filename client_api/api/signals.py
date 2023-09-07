from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, LoanedBook
from .tasks import send_user_data, send_loaned_book_data
from .serializers import BookSerializer, UserSerializer


@receiver(post_save, sender=User)
def send_user_data_event(sender, **kwargs) -> None:
    user = kwargs["instance"]
    created = kwargs["created"]

    # Call the celery task to send data to the admin_api service
    send_user_data.delay(user.id, user.email, user.first_name, user.last_name, created)


@receiver(post_save, sender=LoanedBook)
def send_loaned_book_data_event(sender, **kwargs) -> None:
    loaned_book: LoanedBook = kwargs["instance"]

    
    send_loaned_book_data.apply_async(
        kwargs={
            "date_borrowed": loaned_book.date_borrowed,
            "return_date": loaned_book.return_date,
            "book_id": loaned_book.book.id,
            "user_id": loaned_book.user.id,
        }
    )
