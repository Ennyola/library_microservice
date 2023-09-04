from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .tasks import send_user_data


@receiver(post_save, sender=User)
def send_user_data_event(sender, **kwargs) -> None:
    user = kwargs["instance"]
    created = kwargs["created"]
    # Call the celery task to send data to the admin_api service
    send_user_data.delay(user.id, user.email, user.first_name, user.last_name, created)
