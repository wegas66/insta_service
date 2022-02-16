from django import forms
from .models import TaskParseLikes, TaskParseSubscribers


class TaskParseLikesForm(forms.ModelForm):
    class Meta:
        model = TaskParseLikes
        fields = ('instagram_user', 'quantity_posts', 'quantity_users')


class TaskParseSubscribersForm(forms.ModelForm):
    class Meta:
        model = TaskParseSubscribers
        fields = ('instagram_users', 'quantity_users')
