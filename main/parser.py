from instabot import Bot, utils
from .models import IGAccount
import datetime

bot = Bot()


def get_account():
    delta = datetime.datetime.now() - datetime.timedelta(minutes=1)
    account = IGAccount.objects.filter(last_use__lt=delta, in_use=False).order_by('last_use').first()
    return account


def parser(users, nfollows):
    acc = get_account()
    users = users.replace(' ', '').split(',')
    #make account in use
    acc.in_use = True
    acc.save()
    try:
        parsed_data = parse_followers(acc, users, nfollows)

    except Exception as e:
        print(e)
        return False
    finally:
        #make account not in use and set last use date
        acc.in_use = False
        acc.save()



def parse_followers(acc,nfollows, users):
    bot.login(username=acc.username, password=acc.password)
    f = utils.file('parse.txt')
    followers = []
    for user in users:
        try:
            followers += bot.get_user_followers(user, nfollows=nfollows)
        except Exception as e:
            print(e)
            continue
    f.save_list(followers)
