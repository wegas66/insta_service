import time
from .parser import *
from insta_service.celery import app


@app.task()
def sync_task(nfollows):
    try:
        parse_followers(nfollows)
        return True
    except:
        return False
