# PlivoApp

Using Celery as Task Queue and Redis as broker, this application pushes Message+CallBack URL into the queue where it tries to deliver the message to an external service and also tries to send notification to the CallBack URL if the status of message delivery changes. If the message delivery service or CallBack URL are not up, the respective tasks are retried using an exponential backoff countdown.

To emulate an external service to send message, the API class "DummyExternalService" is implemented which is randomly down. When it is up, the message is considered to be delivered and retry stops.

Similarly, to emulate the callback notification URL service, the API class "DummyUserCallbackService" is implemented which is randomly down. When it is up, the notification is considered to be delivered and retry stops.

Status of message delivery is maintained in the model "TaskStatus" which is also used to discard out of order messages when sending the callback notification to the CallBack URL.
More details about task status and result can be viewed in Celery provided model "TaskMeta".
Both these models are exposed in django admin interface.

Pushing the task to queue: Either the API "PostMessageAPI" can be used or Openshift web interface can be used. 
API Usage Example: resp = requests.post(SITE_URL+reverse("post-message-api"))
Before the task is picked by worker(there is a default ETA/Countdown of 10 seconds for testing purpose), the status is "QUEUED".
Once the task is picked up by worker, status is changed to "SENT" and another task is triggered to send callback notification to the CallBack URL.
If the external services is up, the status changes from "SENT" to "DELIVERED" and another callback notification is triggered. At this point, if previous callback notification task for "SENT" status is not yet completed, then it is revoked so that notification with earlier state is ignored if same message with later state is being processed.




