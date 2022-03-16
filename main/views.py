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
from django.contrib.auth.decorators import login_required



class HomeView(TemplateView):
    template_name = 'insta_app/home.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class TasksView(LoginRequiredMixin, TemplateView):
    template_name = 'insta_app/tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.request.user.task_set.order_by('-timestamp')
        return context


class CreateTaskSubsView(LoginRequiredMixin, CreateView):
    template_name = 'insta_app/parser.html'
    model = TaskParseSubscribers
    form_class = TaskParseSubscribersForm
    success_url = reverse_lazy('main_app:tasks')

    def form_valid(self, form):
        print(form.cleaned_data)
        payment_acc = self.request.user.paymentaccount
        total_sum = TaskParseSubscribers(instagram_users=form.instance.instagram_users, quantity_users=form.instance.quantity_users).total_sum()
        if payment_acc.balance >= total_sum: #хватает ли средств на балансе


            payment = Transaction(user=self.request.user.paymentaccount, reason='SUB', amount=form.instance.quantity_users) #создание транзакции
            payment.save()


            payment_acc.balance -= total_sum #изменение баланса
            payment_acc.save()

            form.instance.user = self.request.user
            form.instance.name = f'Задача "парсинг подписчиков" №'
            form.instance.payment = payment

            return super().form_valid(form)
        else:
            return render(request=self.request, template_name='payments/not_enough_balance.html')

    def get_success_url(self):
        parse.delay(self.object.instagram_users, self.object.quantity_users, self.object.pk)
        return super().get_success_url()


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
            return render(request=self.request, template_name='insta_app/not_enough_balance.html')


class TaskResultView(LoginRequiredMixin, DetailView):
    template_name = 'insta_app/parser.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['third_stage'] = True
        return context
