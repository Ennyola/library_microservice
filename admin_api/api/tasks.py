from celery import shared_task, current_app


@shared_task(name="add")
def add(x, y):
    task_name = "multiply"
    worker = "client_worker"
    current_app.send_task(task_name, args=(x, y))
    return x * y


@shared_task(name="rand")
def rand(y, x):
    return x + y
