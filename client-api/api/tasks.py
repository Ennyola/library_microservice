from celery import shared_task

# Celery Tasks

@shared_task
def multiply(x: int, y: int) -> int:
    return x * y
