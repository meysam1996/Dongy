from django.shortcuts import render
from .models import Invoice
from .seializers import InvoiceSerializer
from rest_framework import viewsets

# Create your views here.
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer