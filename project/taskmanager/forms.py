from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Task
from .widgets import InputCustom, TextareaCustom


class TaskForm(forms.Form):
    # user = forms.ForeignKey()
    new_task_id = forms.IntegerField(required=False)
    new_task_title = forms.CharField(max_length=200)
    new_task_description = forms.CharField(max_length=1000)
    image = forms.ImageField(required=False)
    # video = forms.FileField()
    new_task_deadline = forms.DateField(required=False)
    new_task_state = forms.IntegerField()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     task_id = cleaned_data.get('new_task_id')
    #     title = cleaned_data.get('new_task_title')
    #     description = cleaned_data.get('new_task_description')
    #     deadline_str = cleaned_data.get('new_task_deadline')
    #     state_str = cleaned_data.get('new_task_state')
    #
    #     if not title and not description and not state_str:
    #         raise ValidationError('Some fields are required')
    #
    #     # if task_id and not Task.objects.get(id=task_id).exists():
    #     #     raise ValidationError('Task does not exist')
    #
    #     try:
    #         state = int(state_str)
    #     except:
    #         raise forms.ValidationError('State must be an integer')
    #
    #     try:
    #         if deadline_str:
    #             deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
    #     except:
    #         raise forms.ValidationError('Wrong Date Format')
    #
    #     return cleaned_data
