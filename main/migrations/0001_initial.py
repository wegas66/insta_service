# Generated by Django 3.2.8 on 2022-03-29 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='IGAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('last_use', models.DateTimeField(auto_now=True)),
                ('in_use', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Задача', max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('result', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('payment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='payments.transaction')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_main.task_set+', to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='TaskParseLikes',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.task')),
                ('posts', models.TextField()),
                ('quantity_users', models.PositiveIntegerField(default=1)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('main.task',),
        ),
        migrations.CreateModel(
            name='TaskParseSubscribers',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.task')),
                ('instagram_users', models.TextField()),
                ('quantity_users', models.PositiveIntegerField(default=1)),
                ('task_type', models.CharField(choices=[('FR', 'Followers'), ('FG', 'Following')], default='FR', max_length=2)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('main.task',),
        ),
    ]
