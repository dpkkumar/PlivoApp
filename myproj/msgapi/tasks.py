from celery.decorators import task
from celery.task.control import revoke
from myproj.settings import MAX_RETRIES
from models import TaskStatus
import requests


def add_msg_to_queue(message, url):
    # Push the task to queue with a delay of 10 seconds
    async_task = enqueue_and_retry.apply_async((message, url), countdown=10)
    TaskStatus.objects.create(task_id=async_task.task_id, status=TaskStatus.QUEUED)
    return async_task


@task(max_retries=MAX_RETRIES)
def enqueue_and_retry(msg, url):
    from api import DummyExternalService
    external_service_response = DummyExternalService.post(msg)
    status_code = external_service_response['status_code']

    # Update task status from queued to sent
    task_id = enqueue_and_retry.request.id
    task_status = TaskStatus.objects.get(task_id=task_id)
    if task_status.status == TaskStatus.QUEUED:
        task_status.status = TaskStatus.SENT
        task_status.save()
        # Send a callback notification
        send_callback_notification.apply_async((url, task_id, TaskStatus.SENT), countdown=10)

    # Retry if service is not up
    if status_code == 404:
        # Exponential backoff: 2**0+4, 2**1+4, 2**2+4, 2**3+4, 2**4+4,...
        seconds_to_wait = 2 ** enqueue_and_retry.request.retries + 4
        raise enqueue_and_retry.retry(exc=Exception("Remote Service is Down"), countdown=seconds_to_wait)

    # If service returns acknowledgement(200 status code), message is delivered, so update task status to delivered.
    if task_status.status == TaskStatus.SENT:
        task_status.status = TaskStatus.DELIVERED
        task_status.save()
        # Send a callback notification
        send_callback_notification.apply_async((url, task_id, TaskStatus.DELIVERED), countdown=10)
    return "Message Delivered Successfully"


@task(max_retries=MAX_RETRIES)
def send_callback_notification(url, message_task_id, status):
    # Check the current status of task and if it has moved on to next state, terminate the current task.
    task_status = TaskStatus.objects.get(task_id=message_task_id)
    if task_status.status != status:
        curr_task_id = send_callback_notification.request.id
        revoke(curr_task_id, terminate=True)

    # Try posting the notification and retry if not successful.
    try:
        response = requests.post(url, data={'task_id': message_task_id, 'status': status})
        if response.status_code == 404:
            raise Exception("User callback service is down for URL: {}.".format(url))
        print response.text
    except Exception as e:
        # Exponential backoff: 2**0+4, 2**1+4, 2**2+4, 2**3+4, 2**4+4,...
        seconds_to_wait = 2 ** send_callback_notification.request.retries + 4
        raise enqueue_and_retry.retry(exc=e, countdown=seconds_to_wait)
    return "Notification Sent to URL: {} for MessageTaskID: {} with Status: {}".format(url, message_task_id, status)
