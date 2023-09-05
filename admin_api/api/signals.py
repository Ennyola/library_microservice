from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Book
from .serializers import BookSerializer
from .tasks import send_new_book_data

@receiver(post_save, sender=Book)
def send_new_book_data_event(sender, **kwargs):
    book = kwargs["instance"]
    created = kwargs["created"]
    
    serialized_book = BookSerializer(book)
    send_new_book_data.apply_async(kwargs={"created":created, **serialized_book.data})