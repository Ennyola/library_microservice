from celery import shared_task


@shared_task
def add(x, y):
    result = send_task("multiply", args=(x,y))
    return result
