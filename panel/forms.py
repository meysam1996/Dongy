from django import forms
from panel.models import Invoice, People, Transaction


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['name']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'price']

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        invoice = kwargs.get('pk')
        if invoice:
            self.fields['payer'].queryset = People.objects.filter(invoice = invoice)