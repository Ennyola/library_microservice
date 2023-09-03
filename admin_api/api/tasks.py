from celery import shared_task, current_app

@shared_task(name="fetch_users")
def fetch_users():
    # Get users from client_api 
    return current_app.send_task("get_users")
   