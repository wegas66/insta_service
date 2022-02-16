from django.shortcuts import render, redirect
from .models import TaskParseLikes, TaskParseSubscribers, Task
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from .forms import TaskParseSubscribersForm, TaskParseLikesForm
import datetime




class HomeView(TemplateView):
    template_name = 'main/home.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class TasksView(LoginRequiredMixin, TemplateView):
    template_name = 'main/tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.request.user.task_set.order_by('-timestamp')
        return context


class CreateTaskSubsView(LoginRequiredMixin, CreateView):
    template_name = 'main/create_task_subs_form.html'
    model = TaskParseSubscribers
    form_class = TaskParseSubscribersForm
    success_url = reverse_lazy('main_app:tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = f'Задача "парсинг подписчиков" №'
        return super().form_valid(form)


class CreateTaskLikesView(LoginRequiredMixin, CreateView):
    template_name = 'main/create_task_likes_form.html'
    model = TaskParseLikes
    form_class = TaskParseLikesForm
    success_url = reverse_lazy('main_app:tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = f'Задача "парсинг лайков" №'
        return super().form_valid(form)


class TaskResultView(LoginRequiredMixin, DetailView):
    template_name = 'main/task_result.html'
    model = Task

