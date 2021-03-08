from django import forms
from panel.models import Invoice, People, Transaction


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['name']

