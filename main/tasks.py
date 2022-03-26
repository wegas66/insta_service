import time
from .parser import run_parser
from insta_service.celery import app
from .models import *


@app.task()
def parse(pk):
    try:
        run_parser(pk)
        return True
    except Exception as e:
        print(e)
        return False
