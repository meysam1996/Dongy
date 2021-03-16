from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.edit import FormView

from panel.models import Invoice, People, Transaction
from panel.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from panel.forms import InvoiceForm, TransactionForm, PeopleForm


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
    # model = Transaction
    form_class = TransactionForm
    template_name = 'panel/action_form.html'

    def get_success_url(self):
        return reverse_lazy('panel:invoice_detail_actions', args=[self.invoice.id])

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ActionCreateView, self).get_form_kwargs(*args, **kwargs)
        self.invoice = get_object_or_404(Invoice, id = self.kwargs['pk'])
        kwargs['pk'] = self.invoice
        return kwargs

    def get_context_data(self, **kwargs):
        self.invoice = get_object_or_404(Invoice, id = self.kwargs['pk'])
        kwargs['invoice'] = self.invoice
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.invoice = get_object_or_404(Invoice, id = self.kwargs['pk'])
        form.instance.owner = self.request.user
        form.instance.invoice = self.invoice
        self.object = form.save(commit=False)
        self.object.save()

        persons = str(self.request.POST.get('persons'))
        persons = persons.split(',')
        pl = []
        for person in persons:
            pl.append(People.objects.get_or_create(name=person))
        self.object.persons.add(pl)
        self.object.save()
        form.save_m2m()

        return super().form_valid(form)

    
class ActionUpdateView(LoginRequiredMixin, View):
    template_name = 'panel/action_form.html'
    success_url = reverse_lazy('panel:invoice_detail_actions')

    def get(self, request, pk):
        Tr = get_object_or_404(Transaction, id=pk, owner = self.request.user)
        form = TransactionForm(instance=Tr)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        Tr = get_object_or_404(Transaction, id=pk, owner= self.request.user)
        form = TransactionForm(request.POST, instance=Tr)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        
        Tr = form.save(commit=False)
        Tr.save()
        return redirect(self.success_url)


class ActionDeleteView(OwnerDeleteView):
    model = Transaction
    template_name = 'panel/action_confirm_delete.html'


class PeopleCreateView(LoginRequiredMixin, CreateView):
    # model = People
    form_class = PeopleForm
    template_name = 'panel/people_form.html'

    def get_success_url(self):
        return reverse('panel:invoice_detail_persons', args=[self.invoice.id])

    def get_context_data(self, **kwargs):
        self.invoice = get_object_or_404(Invoice, id = self.kwargs['pk'])
        kwargs['invoice'] = self.invoice
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.invoice = get_object_or_404(Invoice, id = self.kwargs['pk'])
        form.instance.owner = self.request.user
        form.instance.invoice = self.invoice
        return super().form_valid(form)


class PeopleUpdateView(LoginRequiredMixin, View):
    template_name = 'panel/people_form.html'
    success_url = reverse_lazy('panel:invoice_detail_persons')

    def get(self, request, pk):
        person = get_object_or_404(People, id=pk, owner = self.request.user)
        form = PeopleForm(instance=person)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        person = get_object_or_404(People, id=pk, owner= self.request.user)
        form = PeopleForm(request.POST, instance=person)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        
        person = form.save(commit=False)
        person.save()
        return redirect(self.success_url)


class PeopleDeleteView(OwnerDeleteView):
    model = People
    template_name = 'panel/person_confirm_delete.html'


# class TransactionResultDong(LoginRequiredMixin, View):
#     model = Transaction
#     template_name = 'panel/result_detail_action.html'

#     def get(self, request, pk):
#         price = Transaction.objects.get(id=pk)
#         transactions = Transaction.objects.filter(invoice=Inv).order_by('-updated_at')
#         ctx = {'invoice': Inv, 'transactions': transactions}
#         return render(request, self.template_name, ctx)