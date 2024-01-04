from django.core.serializers import serialize
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm
from .models import Task, TaskState
from accounts.models import UserInfo


def calculate_position(user, previous_id_str, task_state_instance):
    # not previous_id_str -> add new task or update by form => last of array
    if not previous_id_str:
        last_task = Task.objects.filter(user=user, state=task_state_instance).order_by('position').last()
        return last_task.position + 100 if last_task else 0

    # update using ajax
    previous_id = int(previous_id_str)
    if previous_id == -1:
        first_task = Task.objects.filter(user=user, state=task_state_instance).first()
        return first_task.position - 100 if first_task else 0

    previous_task = Task.objects.get(id=previous_id)
    next_task = Task.objects.filter(
        user=user,
        state=task_state_instance,
        position__gt=previous_task.position
    ).order_by('position').first()

    return ((next_task.position - previous_task.position) / 2 + previous_task.position
            if next_task else previous_task.position + 100)


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'taskmanager/index.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_info'] = user
        states = TaskState.objects.all()
        context['states'] = states
        tasks = Task.objects.filter(user=user)
        if 'filter' in self.request.GET:
            key = self.request.GET['filter']
            tasks = tasks.filter(title__icontains=key)
            context['search_key'] = key
        context['tasks'] = tasks
        context['form'] = TaskForm()
        context['tasks_json'] = serialize('json', tasks)
        context['states_json'] = serialize('json', states)
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        previous_id_str = request.POST.get('previous_id')
        if not form.is_valid():
            return redirect('home')
        # get data
        task_id = form.cleaned_data['new_task_id']
        task_state = form.cleaned_data['new_task_state']
        task_description = form.cleaned_data['new_task_description']
        task_title = form.cleaned_data['new_task_title']
        task_deadline = form.cleaned_data['new_task_deadline']
        user = UserInfo.objects.get(id=request.user.id)
        # create or update
        task_state_instance = TaskState.objects.get(id=task_state)
        position = calculate_position(user, previous_id_str, task_state_instance)
        task_data = {
            'user': user,
            'state': task_state_instance,
            'description': task_description,
            'title': task_title,
            'deadline': task_deadline,
            'position': position
        }
        if not task_id:
            task_id = None
        task, created = Task.objects.update_or_create(
            id=task_id,
            defaults=task_data
        )
        print(f'state: {task_state_instance.name}')
        task.save()
        return redirect('home')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('home')
    template_name = "taskmanager/confirm_delete_task.html"
