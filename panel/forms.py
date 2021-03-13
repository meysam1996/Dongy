from django import forms
from django.shortcuts import get_object_or_404
from panel.models import Invoice, People, Transaction


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['name']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'price', 'payer']

    def __init__(self, *args, **kwargs):
        invoice = kwargs.pop('pk')
        super().__init__(*args, **kwargs)
        self.fields['payer'].queryset = People.objects.filter(invoice=invoice)


class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = ['name', 'username', 'active', 'phone_number']