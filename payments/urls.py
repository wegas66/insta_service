from django.urls import path, include
from .views import CreateInvoiceView

app_name = 'payments'

urlpatterns = [
    path('balance_add', CreateInvoiceView.as_view(), name='balance_add'),
]
