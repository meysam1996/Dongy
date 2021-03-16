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

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['payer'].queryset = People.objects.filter(invoice=self.pk)
        self.fields['persons'] = forms.ModelMultipleChoiceField(
        queryset=People.objects.filter(invoice=self.pk),
        widget=forms.CheckboxSelectMultiple
        )


class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = ['name', 'username', 'active', 'phone_number']