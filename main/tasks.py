import time
from .parser import run_parser
from insta_service.celery import app


@app.task()
def parse(users, nfollows, pk):
    try:
        run_parser(users, nfollows, pk)
        return True
    except Exception as e:
        print(e)
        return False
