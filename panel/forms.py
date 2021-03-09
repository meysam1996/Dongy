from django import forms
from panel.models import Invoice, People, Transaction


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['name']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'price', 'payer']