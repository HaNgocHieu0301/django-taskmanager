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

    # def post(self, request, *args, **kwargs):
    #     form = TaskForm(request.POST)
    #     previous_position_str = request.POST.get('previous_position')
    #     next_position_str = request.POST.get('next_position')
    #     print('check change position')
    #     print(previous_position_str)
    #     print(next_position_str)
    #     if form.is_valid():
    #         # get data
    #         task_id = form.cleaned_data['new_task_id']
    #         task_state = form.cleaned_data['new_task_state']
    #         task_description = form.cleaned_data['new_task_description']
    #         task_title = form.cleaned_data['new_task_title']
    #         task_deadline = form.cleaned_data['new_task_deadline']
    #         # create or update
    #         task_state_instance = TaskState.objects.get(id=task_state)
    #         if not task_id:
    #             task_id = None
    #         (task, flag) = Task.objects.get_or_create(id=task_id)
    #         task.state = task_state_instance
    #         task.description = task_description
    #         task.title = task_title
    #         task.deadline = task_deadline
    #
    #         print('now position')
    #         print(task.position)
    #         # update position for task
    #         if not next_position_str and not previous_position_str:
    #             """
    #                 add new task
    #             """
    #             print('vvv 1')
    #             last_task = Task.objects.filter(user=request.user, state=task_state_instance).last()
    #             if last_task:
    #                 # add last
    #                 task.position = last_task.position + 100
    #             else:
    #                 # add when no having task
    #                 task.position = 0
    #         elif not next_position_str:
    #             """
    #                 update task - move go to the last array
    #             """
    #             print('vvv 2')
    #             task.position = round(float(previous_position_str)) + 100
    #         elif not previous_position_str:
    #             """
    #                 update task - move go to the beginning array
    #             """
    #             print('vvv 3')
    #             task.position = round(float(next_position_str)) - 100
    #         else:
    #             """
    #                 update task - move go to middle array
    #             """
    #             print('vvv 4')
    #             next_position = float(next_position_str)
    #             previous_position = float(previous_position_str)
    #             if abs(next_position - previous_position) > 2 and next_position_str:
    #                 task.position = previous_position - 1
    #             else:
    #                 task.position = (next_position + previous_position) / 2 - previous_position
    #
    #         # if task_id:
    #         #     task.id = int(task_id)
    #         task.save()
    #         print('after')
    #         print(task.position)
    #         return redirect('home')
    #     return redirect('home')

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        previous_id_str = request.POST.get('previous_id')
        if form.is_valid():
            print('----------------------------------check--------------------------')
            print(previous_id_str)
            # get data
            task_id = form.cleaned_data['new_task_id']
            task_state = form.cleaned_data['new_task_state']
            task_description = form.cleaned_data['new_task_description']
            task_title = form.cleaned_data['new_task_title']
            task_deadline = form.cleaned_data['new_task_deadline']
            # create or update
            task_state_instance = TaskState.objects.get(id=task_state)
            if not task_id:
                task_id = None
            (task, flag) = Task.objects.get_or_create(id=task_id)
            task.state = task_state_instance
            task.description = task_description
            task.title = task_title
            task.deadline = task_deadline
            # check last task with specific state
            last_task = Task.objects.filter(user=request.user, state=task_state_instance).order_by('position').last()
            # update position for task in column with specific state
            if not last_task:
                """
                    add new task in empty list
                """
                # add when no having task
                task.position = 0
                print('vvv1')
            elif not previous_id_str:
                task.position = round(last_task.position) + 100
            else:
                previous_id = int(previous_id_str)
                if previous_id == -1:
                    print('vvv2')
                    """
                        update task - move go to the beginning of the list
                    """
                    first_task = Task.objects.filter(user=request.user, state=task_state_instance).first()
                    task.position = round(first_task.position) - 100
                elif previous_id == last_task.id:
                    print('vvv3')
                    """
                        update task - move go to the last of the list
                    """
                    task.position = round(last_task.position) + 100
                else:
                    print('vvv4')
                    previous_task = Task.objects.get(id=previous_id)
                    next_task = (Task.objects.get(user=request.user, state=task_state_instance,
                                                  position__gt=previous_task.position))
                    if next_task:
                        if abs(next_task.position - previous_task.position) > 2:
                            print('vvv4.1')
                            task.position = previous_task.position + 1
                        else:
                            print('vvv4.2')
                            task.position = (next_task.position + previous_task.position) / 2 - previous_task.position
            task.save()
            print(f'new pos: {task.position}')
            return redirect('home')
        return redirect('home')

class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('home')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        return super().delete(*args, **kwargs)


