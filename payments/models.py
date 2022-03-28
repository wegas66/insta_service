from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=300)

    def change_balance(self, amount):
        self.balance += amount

class Transaction(models.Model):
    ADD = 'ADD'
    SUBTRACT = 'SUB'
    REASON_CHOICES = [
        (ADD, 'Add to balance'),
        (SUBTRACT, 'Subtract from balance')
    ]

    user = models.ForeignKey(PaymentAccount, related_name='balance_changes', on_delete=models.PROTECT)
    reason = models.CharField(choices=REASON_CHOICES, max_length=3)
    amount = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)




class Invoice(models.Model):
    user = models.ForeignKey(PaymentAccount, on_delete=models.PROTECT)
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, blank=True, null=True)
    amount = models.PositiveIntegerField(default=1000)
    paid = models.BooleanField(default=False)
    invoice_label = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)