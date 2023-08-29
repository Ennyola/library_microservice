from celery import Celery

app = Celery("shared_tasks")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

# Import the shared tasks from tasks.py
from .tasks import add
