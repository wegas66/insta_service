import time
from .parser import *
from insta_service.celery import app


@app.task()
def parse(users, nfollows):
    try:
        parse_followers(users, nfollows)
        return True
    except Exception as e:
        print(e)
        return False
