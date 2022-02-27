from django.shortcuts import render, redirect
from .models import TaskParseLikes, TaskParseSubscribers, Task
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, get_user_model
from django.urls import reverse_lazy
from .forms import TaskParseSubscribersForm, TaskParseLikesForm
from payments.models import Transaction
from .tasks import parse




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
        payment_acc = self.request.user.paymentaccount
        total_sum = TaskParseSubscribers(instagram_users=form.instance.instagram_users, quantity_users=form.instance.quantity_users).total_sum()
        if payment_acc.balance >= total_sum: #хватает ли средств на балансе


            payment = Transaction(user=self.request.user.paymentaccount, reason='SUB', amount=form.instance.quantity_users) #создание транзакции
            payment.save()

            parse.delay(form.instance.instagram_users, form.instance.quantity_users)

            payment_acc.balance -= total_sum #изменение баланса
            payment_acc.save()

            form.instance.user = self.request.user
            form.instance.name = f'Задача "парсинг подписчиков" №'
            form.instance.payment = payment

            return super().form_valid(form)
        else:
            return render(request=self.request, template_name='payments/not_enough_balance.html')


class CreateTaskLikesView(LoginRequiredMixin, CreateView):
    template_name = 'main/create_task_likes_form.html'
    model = TaskParseLikes
    form_class = TaskParseLikesForm
    success_url = reverse_lazy('main_app:tasks')

    def form_valid(self, form):
        payment_acc = self.request.user.paymentaccount
        total_sum = TaskParseLikes(quantity_posts=form.instance.quantity_posts, quantity_users=form.instance.quantity_users).total_sum()
        if payment_acc.balance >= total_sum: #хватает ли средств на балансе
            payment = Transaction(user=self.request.user.paymentaccount, reason='SUB', amount=form.instance.quantity_users) #создание транзакции
            payment.save()

            payment_acc.balance -= total_sum #изменение баланса
            payment_acc.save()

            form.instance.user = self.request.user
            form.instance.name = f'Задача "парсинг лайков" №'
            return super().form_valid(form)
        else:
            return render(request=self.request, template_name='payments/not_enough_balance.html')


class TaskResultView(LoginRequiredMixin, DetailView):
    template_name = 'main/task_result.html'
    model = Task



