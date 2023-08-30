from celery import shared_task, current_app

from shared_tasks.client_tasks import multiply


@shared_task
def add(x, y):
   return multiply(x,y)
