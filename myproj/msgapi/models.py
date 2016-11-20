from django.db import models
import datetime


class TaskStatus(models.Model):
    QUEUED = 'queued'
    SENT = 'sent'
    DELIVERED = 'delivered'
    STATUS = (
        (QUEUED, 'QUEUED'),
        (SENT, 'SENT'),
        (DELIVERED, 'DELIVERED'),
    )

    task_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
    status = models.CharField(max_length=50, choices=STATUS)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    def __unicode__(self):
        return self.task_id

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created_on = datetime.datetime.now()
        self.updated_on = datetime.datetime.now()
        return super(TaskStatus, self).save(*args, **kwargs)
