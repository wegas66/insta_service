from django.urls import path, include
from .views import CreateInvoiceView, payment_success

app_name = 'payments'

urlpatterns = [
    path('payment/', CreateInvoiceView.as_view(), name='balance_add'),
    path('payment/success', payment_success, name='payment_success'),
]
