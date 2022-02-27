import time
from .parser import *
from insta_service.celery import app


@app.task()
def parse(users, nfollows, pk):
    try:
        parse_followers(users, nfollows, pk)
        return True
    except Exception as e:
        print(e)
        return False
