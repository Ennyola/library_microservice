from celery import shared_task, current_app


@shared_task
def add(x, y):
    multiply.delay(3, 4)
