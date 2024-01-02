from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm
from .models import Task, TaskState
from accounts.models import UserInfo


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'taskmanager/index.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_info'] = user
        states = TaskState.objects.all()
        context['states'] = states
        if 'filter' in self.request.GET:
            key = self.request.GET['filter']
            tasks = Task.objects.filter(title__icontains=key)
            context['search_key'] = key
        else:
            tasks = Task.objects.filter(user=user)
        context['tasks'] = tasks
        context['form'] = TaskForm()
        context['tasks_json'] = serialize('json', tasks)
        context['states_json'] = serialize('json', states)
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data['new_task_id']
            task_state = form.cleaned_data['new_task_state']
            task_description = form.cleaned_data['new_task_description']
            task_title = form.cleaned_data['new_task_title']
            task_deadline = form.cleaned_data['new_task_deadline']
            if task_id:
                task = Task.objects.get(id=task_id)
                task.state = TaskState.objects.get(id=task_state)
                task.description = task_description
                task.title = task_title
                if task_deadline:
                    task.deadline = task_deadline
                task.modified_at = timezone.now()
                task.save()
            else:
                user = UserInfo.objects.get(id=request.user.id)
                task_state_instance = TaskState.objects.get(id=task_state)
                task = Task(user=user, state=task_state_instance, description=task_description,
                            title=task_title, deadline=task_deadline)
                task.modified_at = timezone.now()
                task.save()
            return redirect('home')
        print('form is not valid')
        return redirect('home')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('home')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        return super().delete(*args, **kwargs)


