from celery.decorators import task
import urllib
from myproj.settings import MAX_RETRIES


@task(default_retry_delay=5, max_retries=MAX_RETRIES)
def add_msg_to_q(msg, url):
    # add msg to db
    print "============================================test==================="
    try:
        urllib.urlopen(url)
    except Exception, e:
        raise add_msg_to_q.retry(exc=e)
    return 'done'
