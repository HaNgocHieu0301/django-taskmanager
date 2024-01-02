from django.contrib import admin
from django.db import models
from accounts.models import UserInfo
from django import forms


class TaskState(models.Model):
    class Meta:
        """
            Change name of table in admin interface
        """
        verbose_name = 'Task\'s State'
        verbose_name_plural = 'Task\'s State'

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#     # projects = models.ManyToManyField('Task', blank=True, null=True)
#
#     def __str__(self):
#         return str(self.name)


class Task(models.Model):
    user = models.ForeignKey(UserInfo, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='static/images', blank=True, null=True)
    video = models.FileField(upload_to='static/videos', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField(blank=True, null=True)
    state = models.ForeignKey(TaskState, on_delete=models.CASCADE, related_name='tasks')
    # tags = models.ManyToManyField('Tag')

    def __str__(self):
        return f'{self.title}'

