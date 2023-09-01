from celery import shared_task, current_app


@shared_task(name="add")
def add(x, y):
    task_name = "multiply"
    current_app.send_task(task_name, args=(x, y))
    return x * y
