from django.contrib.auth import get_user_model
from django.db import models
from polymorphic.models import PolymorphicModel

User = get_user_model()


class Task(PolymorphicModel):
    name = models.CharField(max_length=200, default='Задача')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    result = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return f'{self.name}{self.pk}'


class TaskParseSubscribers(Task):
    instagram_users = models.TextField()
    quantity_users = models.PositiveIntegerField(default=1)


class TaskParseLikes(Task):
    instagram_user = models.TextField()
    quantity_posts = models.PositiveIntegerField(default=1)
    quantity_users = models.PositiveIntegerField(default=1)

