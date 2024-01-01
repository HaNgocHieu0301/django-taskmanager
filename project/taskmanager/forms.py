from django import forms
from django.utils import timezone

from .models import Task
from .widgets import InputCustom, TextareaCustom


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['__all__']
        widgets = {
            'title': InputCustom(attrs={'placeholder': 'Task', 'title': 'Task'}),
            'description': TextareaCustom(attrs={'placeholder': 'Description', 'title': 'Description'})
        }

    def save(self, commit=True, *args, **kwargs):
        m = super().save(commit=False)
        m.modified_at = timezone.now()
        if commit:
            m.save()
        return m
