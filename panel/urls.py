from django.urls import path, reverse_lazy
from . import views

app_name='panel'
urlpatterns = [
    # path('', views.InviceListView.as_view()),
    path('Invoices', views.InviceListView.as_view(), name='all'),
    path('Invoice/<int:pk>/actions', views.InvoiceDetailActionsView.as_view(), name='invoice_detail_actions'),
    path('Invoice/<int:pk>/persons', views.InvoiceDetailPeopleView.as_view(), name='invoice_detail_persons'),
    path('Invoice/create',
        views.InvoiceCreateView.as_view(success_url=reverse_lazy('panel:all')), name='invoice_create'),
    path('Invoice/<int:pk>/update',
        views.InvoiceUpdateView.as_view(success_url=reverse_lazy('panel:all')), name='invoice_update'),
    path('Invoice/<int:pk>/delete',
        views.InvoiceDeleteView.as_view(success_url=reverse_lazy('panel:all')), name='invoice_delete'),
    path('Invoice/<int:pk>/createAction',
        views.ActionCreateView.as_view(success_url=reverse_lazy('panel:all')), name='transaction_create'),
]