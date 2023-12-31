from django.db import models
from accounts.models import UserInfo


class TaskState(models.Model):
    name = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Task(models.Model):
    user = models.ForeignKey(UserInfo, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images', null=True)
    video = models.FileField(upload_to='static/videos', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True)
    state = models.ForeignKey(TaskState, on_delete=models.CASCADE, related_name='tasks')
    tags = models.ManyToManyField(Tag, related_name='tasks')



