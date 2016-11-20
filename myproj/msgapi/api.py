from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from msgapi.tasks import add_msg_to_queue
from djcelery.models import TaskMeta
from models import TaskStatus
import random

import logging
logger = logging.getLogger('django')


class PostMessageAPI(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PostMessageAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        message = request.POST.get('message', None)
        url = request.POST.get('url', None)

        if not message or not url:
            return JsonResponse({"response_details": {"status_code": 100,
                                                      "message": "Please specify the Message and URL."}})

        async_task = add_msg_to_queue(message, url)
        logger.debug("Message: {}, URL: {} pushed to queue with task id:{}".format(message, url, async_task.id))
        return JsonResponse({
            "response_details": {
                "status_code": 200,
                "message": 'Your message is added to the queue with Task ID:{}'.format(async_task.id)
            }})


class MessageStatusAPI(View):
    def get(self, request):
        task_id = request.GET.get('taskid', None)

        if not task_id:
            return JsonResponse({"response_details": {"status_code": 100,
                                                      "message": "Please specify the TaskID."}})

        try:
            task = TaskMeta.objects.get(task_id=task_id)
        except TaskMeta.DoesNotExist:
            return JsonResponse({
                "response_details": {
                    "status_code": 200,
                    "message": 'No task exists with Task ID:{}'.format(task_id)
                }})
        else:
            task_status = TaskStatus.objects.filter(task_id=task_id).values_list('status', flat=True)[0]
            return JsonResponse({
                "response_details": {
                    "status_code": 200,
                    "message": 'Task Details: Status={}, Result={}'.format(task_status, task.result)
                }})


class DummyExternalService(object):
    """
        This class emulates a dummy external service which acknowledges for the posted message with status_code=200,
        but it can be also down sometimes and returns status_code=404.
    """
    @classmethod
    def post(cls, message):
        # To simulate whether service is up or not, consider a random probability.
        is_service_up = random.choice([True, False, 0, ""])

        if not is_service_up:
            return {"status_code": 404}

        cls.do_something_with_message(message)

        return {"status_code": 200}

    @classmethod
    def do_something_with_message(cls, message):
        print message


class DummyUserCallbackService(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(DummyUserCallbackService, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        # To simulate whether service is up or not, consider a random probability.
        is_service_up = random.choice([True, False, 0, ""])

        if not is_service_up:
            return JsonResponse({
                "response_details": {
                    "status_code": 404,
                    "message": "Service down"
                }})

        task_id = request.POST.get('task_id', None)
        status = request.POST.get('status', None)
        logger.debug("Received Notification for TaskID:{} with Status:{}".format(task_id, status))
        return JsonResponse({
            "response_details": {
                "status_code": 200,
                "message": "Received Notification for TaskID:{} with Status:{}".format(task_id, status)
            }})
