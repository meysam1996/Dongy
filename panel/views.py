from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from panel.models import Invoice, People, Transaction
from panel.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from panel.forms import InvoiceForm, TransactionForm

# Create your views here.
class InviceListView(OwnerListView):
    model = Invoice
    template_name = "panel/invoice_list.html"

    def get(self, request):
        invoice_list = Invoice.objects.all()
        ctx = {'invoice_list': invoice_list}

        return render(request, self.template_name, ctx)


class InvoiceDetailActionsView(OwnerDetailView):
    model = Invoice
    template_name = 'panel/invoice_detail_action.html'

    def get(self, request, pk):
        Inv = Invoice.objects.get(id=pk)
        transactions = Transaction.objects.filter(invoice=Inv).order_by('-updated_at')
        ctx = {'invoice': Inv, 'transactions': transactions}
        return render(request, self.template_name, ctx)


class InvoiceDetailPeopleView(OwnerDetailView):
    model = Invoice
    template_name = 'panel/invoice_detail_people.html'

    def get(self, request, pk):
        Inv = Invoice.objects.get(id=pk)
        persons = People.objects.filter(invoice=Inv).order_by('-name')
        ctx = {'invoice': Inv, 'persons': persons}
        return render(request, self.template_name, ctx)


class InvoiceCreateView(LoginRequiredMixin, View):
    template_name = 'panel/invoice_form.html'
    success_url = reverse_lazy('panel:all')

    def get(self, request):
        form = InvoiceForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = InvoiceForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        Inv = form.save(commit=False)
        Inv.owner = self.request.user
        Inv.save()
        return redirect(self.success_url)


class InvoiceUpdateView(LoginRequiredMixin,View):
    template_name = 'panel/invoice_form.html'
    success_url = reverse_lazy('panel:all')

    def get(self, request, pk):
        Inv = get_object_or_404(Invoice, id=pk, owner= self.request.user)
        form = InvoiceForm(instance=Inv)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        Inv = get_object_or_404(Invoice, id=pk, owner= self.request.user)
        form = InvoiceForm(request.POST, instance=Inv)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        Inv = form.save(commit=False)
        Inv.save()
        return redirect(self.success_url)


class InvoiceDeleteView(OwnerDeleteView):
    model = Invoice


class ActionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['name', 'price', 'payer']
    template_name = 'panel/action_form.html'
    success_url = reverse_lazy('panel:all')

    def get(self, request, *args, **kwargs):
        self.invoice = Invoice.objects.get(id=self.kwargs['invoice_id'])
        return super(ActionCreateView, self).get(request, *args, **kwargs)

    def post(self, request, pk=None):
        Inv = get_object_or_404(Invoice, id=pk, owner= self.request.user)
        form = InvoiceForm(request.POST, instance=Inv)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        Inv = form.save(commit=False)
        Inv.save()
        return redirect(self.success_url)