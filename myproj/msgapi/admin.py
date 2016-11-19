from django.contrib import admin
from djcelery.models import TaskMeta


class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)
    list_display = ['date_done', 'task_id', 'status', 'result']


admin.site.register(TaskMeta, TaskMetaAdmin)
