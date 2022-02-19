from yoomoney import Client, Quickpay
from .models import Invoice, Transaction

token = ''
client = Client(token)
user = client.account_info()


def get_operation_url(sum, label):
    quickpay = Quickpay(
        receiver="410011046054185",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=sum,
        label=f"{label}"
    )
    return quickpay.base_url


def is_operation_success(label):
    history = client.operation_history(label=f"{label}")
    for operation in history.operations:
        if 'success' in operation.status:
            return True
        return False


def check_payment(label):
    if is_operation_success(label):
        invoice = Invoice.objects.get(invoice_label=label)
        transaction = Transaction(user=invoice.user, reason='ADD', amount=invoice.amount) #создаем транзакцию
        transaction.save()

        invoice.user.change_balance(invoice.amount)
        invoice.user.save()

        invoice.transaction = transaction
        invoice.paid = True
        invoice.save() #обновляем invoice
        return True
    return False