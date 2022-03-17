from django.urls import path
from .views import HomeView, TasksView, CreateTaskView, TaskResultView

app_name = 'main_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('parser/tasks/', TasksView.as_view(), name='tasks'),
    path('parser/task/<pk>', TaskResultView.as_view(), name='task_result'),
    path("parser/", CreateTaskView.as_view(), name="parser"),
]