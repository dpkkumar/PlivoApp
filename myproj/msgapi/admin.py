from django.contrib import admin
from djcelery.models import TaskMeta
from models import TaskStatus


class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)
    list_display = ['date_done', 'task_id', 'status', 'result']

    def has_add_permission(self, request, obj=None):
        return False


class TaskStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('task_id', 'status', 'created_on', 'updated_on')
    list_display = readonly_fields

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(TaskMeta, TaskMetaAdmin)
admin.site.register(TaskStatus, TaskStatusAdmin)
