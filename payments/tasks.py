from insta_service.celery import app
from .ymoney import check_payment
import time

@app.task(bind=True, default_retry_delay=30, max_retries=10)
def check_payment_task(self, label):
    if check_payment(label):
        return True
    else:
        time.sleep(30)
        raise self.retry()







