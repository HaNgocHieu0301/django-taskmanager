from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm
from .models import Task, TaskState


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
        context['tasks'] = tasks
        context['form'] = TaskForm()
        # print(TaskForm().title.label_tag)
        context['tasks_json'] = serialize('json', tasks)
        context['states_json'] = serialize('json', states)
        # tasks =
        # print('-----------------check information--------------')
        # print(Task.objects.all()[0].tags.all())
        # print(tasks[0])
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})



