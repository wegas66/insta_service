from django import forms
from .models import TaskParseLikes, TaskParseSubscribers


class TaskParseLikesForm(MultipleForm):
    class Meta:
        model = TaskParseLikes
        fields = ('instagram_user', 'quantity_posts', 'quantity_users')


class TaskParseSubscribersForm(MultipleForm):
    class Meta:
        model = TaskParseSubscribers
        fields = ('instagram_users', 'quantity_users')


class TaskMultipleForm(forms.Form):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())


class ContactForm():
    title = forms.CharField(max_length=150)
    message = forms.CharField(max_length=200, widget=forms.TextInput)


class SubscriptionForm(MultipleForm):
    email = forms.EmailField()