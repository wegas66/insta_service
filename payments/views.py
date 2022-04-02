import hashlib
import requests
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .forms import CreateInvoiceForm
from .models import Invoice, Transaction
from .ymoney import get_operation_url
import uuid
import os
from .tasks import check_payment_task
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from dotenv import load_dotenv

load_dotenv()

class CreateInvoiceView(LoginRequiredMixin, CreateView):
    form_class = CreateInvoiceForm
    template_name = 'insta_app/payment.html'

    def form_valid(self, form):
        label = uuid.uuid4()
        form.instance.user = self.request.user.paymentaccount
        form.instance.invoice_label = str(label)
        self.success_url = get_operation_url(form.instance.amount, str(label))
        # check_payment_task.delay(label)
        return super().form_valid(form)



class YooMoneyNotifications(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        requests.get(f'https://api.telegram.org/bot{os.getenv("TG_BOT")}/sendMessage?chat_id=727215391&text={data}')
        s = f'{data["notification_type"]}&{data["operation_id"]}&{data["amount"]}&{data["currency"]}&{data["datetime"]}&{data["sender"]}&{data["codepro"]}&{os.getenv("YOOMONEY_SECRET")}&{data["label"]}'
        s = str.encode(s)
        hash_object = hashlib.sha1(s)
        hash_str = hash_object.hexdigest()
        requests.get(
            f'https://api.telegram.org/bot{os.getenv("TG_BOT")}/sendMessage?chat_id=727215391&text={hash_str}')
        if hash_object != data['sha1_hash']:
            return HttpResponse(status=200)

        invoice = Invoice.objects.get(invoice_label=data['label'])
        transaction = Transaction(user=invoice.user, reason='ADD', amount=invoice.amount)  # создаем транзакцию
        transaction.save()

        invoice.user.change_balance(invoice.amount)
        invoice.user.save()

        invoice.transaction = transaction
        invoice.paid = True
        invoice.save()  # обновляем invoice

        return HttpResponse(status=200)