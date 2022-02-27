from yoomoney import Client, Quickpay
from .models import Invoice, Transaction

token = '410011046054185.51E05EBAB58C9DD088021434E729E1AF95408B801067A4CC3E2B7EAB51841C4E791AFA59260C05B9AB8674C1571E59FF58E8E05EC177E37EF542A2B72577B0E7CD28F5E03CD8F24D3C1FC8B249949C54038660BB03C93ACEAC3B03D0034318620713FDEDBCE02792354E3135279EFC8471799263129581654ACE98A36C72D93C'
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