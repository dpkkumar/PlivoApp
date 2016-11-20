from django.contrib import admin
from djcelery.models import TaskMeta
from models import TaskStatus


class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)
    list_display = ['formatted_date_done', 'task_id', 'status', 'result']
    ordering = ('-date_done', )

    def has_add_permission(self, request, obj=None):
        return False

    # For date_done field, also show seconds
    def formatted_date_done(self, obj):
        return obj.date_done.strftime("%d %b %Y %H:%M:%S")
    formatted_date_done.short_description = 'Done At'


class TaskStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('task_id', 'status', 'created_on', 'updated_on')
    list_display = readonly_fields

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(TaskMeta, TaskMetaAdmin)
admin.site.register(TaskStatus, TaskStatusAdmin)
