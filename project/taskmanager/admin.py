from django.contrib import admin
from .models import Task, TaskState


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user')


    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj=obj, **kwargs)
    #     for tag in Tag.objects.all():
    #         form.fields['tags'].fields[tag.name].widget = form.CheckboxInput()
    #     return form


# class TaskTagAdmin(admin.ModelAdmin):
#     list_display = ('id', 'task', 'tag')


# admin.site.register(Tag)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskState)
# admin.site.register(TaskTag, TaskTagAdmin)

admin.site.site_header = 'Task Manager Admin'
admin.site.site_title = 'Task Manager'
admin.site.index_title = 'INDEX TITLE'

