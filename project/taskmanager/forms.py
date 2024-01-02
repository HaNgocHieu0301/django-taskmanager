from django import forms
from django.utils import timezone

from .models import Task
from .widgets import InputCustom, TextareaCustom


# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         exclude = ['__all__']
#         widgets = {
#             'title': InputCustom(attrs={'placeholder': 'Task', 'title': 'Task'}),
#             'description': TextareaCustom(attrs={'placeholder': 'Description', 'title': 'Description'})
#         }
#
#     def save(self, commit=True, *args, **kwargs):
#         m = super().save(commit=False)
#         m.modified_at = timezone.now()
#         if commit:
#             m.save()
#         return m

class TaskForm(forms.Form):
    # user = forms.ForeignKey()
    new_task_id = forms.IntegerField(required=False)
    new_task_title = forms.CharField(max_length=200)
    new_task_description = forms.CharField(max_length=1000)
    # image = forms.ImageField()
    # video = forms.FileField()
    # created_at = forms.DateTimeField()
    # modified_at = forms.DateTimeField()
    new_task_deadline = forms.DateField(required=False)
    new_task_state = forms.IntegerField()
    # state = forms.ForeignKey()
