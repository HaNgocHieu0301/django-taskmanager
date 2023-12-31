from django.contrib import admin

from .models import Tag, Task, TaskState

admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(TaskState)
