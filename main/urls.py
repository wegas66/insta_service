from django.urls import path
from .views import HomeView, TasksView, CreateTaskSubsView, CreateTaskLikesView, TaskResultView

app_name = 'main_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('tasks/likes/new', CreateTaskLikesView.as_view(), name='create_task_likes'),
    path('parser/task/<pk>', TaskResultView.as_view(), name='task_result'),
    path("parser/", CreateTaskSubsView.as_view(), name="parser"),
]