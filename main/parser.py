import os

from instagrapi import Client
from .models import IGAccount
from main.models import Task
import datetime
from django.core.files import File


class InstagramAccount:
    def __init__(self, model=IGAccount, cooldown=0):
        self.model = model
        self.cooldown = cooldown
        delta = datetime.datetime.now() - datetime.timedelta(minutes=self.cooldown)
        self.account = self.model.objects.filter(last_use__lt=delta, in_use=False).order_by('last_use').first()
        self.username = self.account.username
        self.password = self.account.password

    def in_use(self):
        self.account.in_use = True
        self.account.save()

    def not_in_use(self):
        self.account.in_use = False
        self.account.save()


class Parser:
    IG_CREDENTIAL_PATH = './ig_accs_settings/'

    def __init__(self, account):
        self._bot = Client()
        self.account = account
        if os.path.exists(self.IG_CREDENTIAL_PATH + self.account.username + '.json'):
            self._bot.load_settings(self.IG_CREDENTIAL_PATH + self.account.username + '.json')
            self._bot.login(username=self.account.username, password=self.account.password)
        else:
            self._bot.login(username=self.account.username, password=self.account.password)
            self._bot.dump_settings(self.IG_CREDENTIAL_PATH + self.account.username + '.json')

        self.parsed_accounts = []

    def parse_followers_or_following(self, users, quantity, task_type):
        for user in users:
            try:
                user_id = self._bot.user_id_from_username(user)
                if task_type == 'FR':
                    parsed_users = self._bot.user_followers(user_id=user_id, amount=quantity)
                elif task_type == 'FG':
                    parsed_users = self._bot.user_following(user_id=user_id, amount=quantity)
            except Exception as e:
                print(e)
                continue
            parsed_users = [user.username for user in parsed_users.values()]
            self.parsed_accounts += parsed_users
        return self.parsed_accounts

    def parse_likes(self, posts, q_users):
        for post in posts:
            try:
                media_pk = self._bot.media_pk_from_url(post)
                users = self._bot.media_likers(media_pk)
                users = [user.username for user in users]
                self.parsed_accounts += users
            except Exception as e:
                print(e)
                continue
        return self.parsed_accounts


class SaveTaskResult:
    def __init__(self, result, task_pk, model=Task):
        self.result = result
        self.task_pk = task_pk
        self.model = model

    def save_result(self):
        with open(f'task_{self.task_pk}.txt', 'a+') as f:
            f.write('\n'.join(self.result))
            task = self.model(pk=self.task_pk)
            task.result = File(f)
            task.completed = True
            task.save()


def run_parser(task_pk):
    task = Task.objects.get(pk=task_pk)
    account = InstagramAccount()
    account.in_use()
    try:
        parser = Parser(account)
        if 'парсинг подписчиков' in task.__str__():
            users = task.instagram_users.replace(' ', '').split(',')
            parsed_data = parser.parse_followers_or_following(users, task.quantity_users, task.task_type)
        elif 'парсинг лайков' in task.__str__():
            parsed_data = parser.parse_likes(task.posts, task.quantity_users)
        task_result = SaveTaskResult(parsed_data, task_pk)
        task_result.save_result()
    except Exception as e:
        print(e)
    finally:
        account.not_in_use()
    return True
