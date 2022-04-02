from django.urls import path, include
from .views import CreateInvoiceView, YooMoneyNotifications

app_name = 'payments'

urlpatterns = [
    path('payment/', CreateInvoiceView.as_view(), name='balance_add'),
    path('payment/success', YooMoneyNotifications.as_view(), name='payment_success'),
]
