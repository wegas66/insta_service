from django.contrib import admin
from .models import Transaction, PaymentAccount

admin.site.register(PaymentAccount)
admin.site.register(Transaction)
