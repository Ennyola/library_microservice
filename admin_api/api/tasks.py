from celery import shared_task, current_app


@shared_task(name="fetch_users")
def fetch_users():
    # Get users from client_api 
    users_result = current_app.send_task("get_users")
    users = users_result.get()
    return users
