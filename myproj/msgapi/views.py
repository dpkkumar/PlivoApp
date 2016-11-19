from django.shortcuts import render
from msgapi.tasks import add_msg_to_q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.contrib import messages

import logging
logger = logging.getLogger('django')


def add_task(request):
    if request.method == 'GET':
        logger.debug("TEST LOG:GET is called")
        return render_to_response('post_message.html', {}, context_instance=RequestContext(request))
    else:
        msg = request.POST.get('message')
        url = request.POST.get('url')
        add_msg_to_q.delay(msg, url)
        return HttpResponse('Added msg: {} to queue'.format(msg))


class PostMessageView(TemplateView):
    """
        This view provides a web interface to post a message to an URL.
    """
    template_name = 'post_message.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message', None)
        url = request.POST.get('url', None)

        if not message or not url:
            messages.error(request, 'Please specify the Message and URL.')
            return HttpResponseRedirect("")

        async_task = add_msg_to_q.delay(message, url)
        logger.debug("Message: {}, URL: {} pushed to queue with task id:{}".format(message, url, async_task.id))
        context = self.get_context_data(**kwargs)
        messages.success(request, 'Your message is added to the queue with Task ID:{}'.format(async_task.id))
        return self.render_to_response(context)
