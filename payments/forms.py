from django import forms
from .models import Invoice


class CreateInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('amount',)
