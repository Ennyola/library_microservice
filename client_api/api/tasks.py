from celery import shared_task

@shared_task(name="multiply")
def multiply(x,y):
    return x+y



