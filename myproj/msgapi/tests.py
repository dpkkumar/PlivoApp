# Unit test cases: Not using django.test.TestCase.

# Setup environment to run a standalone script
import os
import sys
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(PROJECT_DIR)
os.chdir(PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproj.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
import requests
from django.core.urlresolvers import reverse
from msgapi.models import TaskStatus

if settings.ON_OPENSHIFT:
    SITE_URL = "http://myapp-plivoapp.rhcloud.com"
else:
    SITE_URL = "http://127.0.0.1:8001"


class MessageStatusAPITest(object):
    @classmethod
    def without_taskid(cls):
        resp = requests.get(SITE_URL+reverse("message-status-api"))
        assert resp.json()['response_details']['status_code'] == 100
        print "MessageStatusAPITest without_taskid JSON output: {}".format(resp.json())

    @classmethod
    def with_taskid(cls):
        resp = requests.get(SITE_URL+reverse("message-status-api"), params={'taskid': 'some_random_taskid'})
        assert resp.json()['response_details']['status_code'] == 200
        print "MessageStatusAPITest with_taskid JSON output: {}".format(resp.json())

        resp = requests.get(SITE_URL+reverse("message-status-api"), params={'taskid': TaskStatus.objects.latest('id').task_id})
        assert resp.json()['response_details']['status_code'] == 200
        print "MessageStatusAPITest with_taskid JSON output: {}".format(resp.json())


class PostMessageAPITest(object):
    @classmethod
    def without_all_parameters(cls):
        resp = requests.post(SITE_URL+reverse("post-message-api"))
        assert resp.json()['response_details']['status_code'] == 100
        print "PostMessageAPITest without_all_parameters JSON output: {}".format(resp.json())

    @classmethod
    def with_parameters(cls):
        resp = requests.post(
                SITE_URL+reverse("post-message-api"),
                data={'message': 'test message', 'url': SITE_URL+reverse("user-callback-service")})
        assert resp.json()['response_details']['status_code'] == 200
        print "PostMessageAPITest with_parameters JSON output: {}".format(resp.json())

if __name__ == '__main__':
    MessageStatusAPITest.without_taskid()
    MessageStatusAPITest.with_taskid()
    PostMessageAPITest.without_all_parameters()
    PostMessageAPITest.with_parameters()
