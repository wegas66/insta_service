from django.urls import path
from .views import HomeView, TasksView, CreateTaskSubsView, CreateTaskLikesView, TaskResultView, parser_page, payment

app_name = 'main_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('tasks/subscribers/new', CreateTaskSubsView.as_view(), name='create_task_subs'),
    path('tasks/likes/new', CreateTaskLikesView.as_view(), name='create_task_likes'),
    path('task/<pk>', TaskResultView.as_view(), name='task_result'),
    path("parser/", parser_page, name="parser"),
    path("payment/", payment, name='payment'),
]