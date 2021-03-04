from django.contrib import admin
from .models import People, Invoice, Transaction

# Register your models here.

admin.site.register(Invoice)
admin.site.register(Transaction)
admin.site.register(People)
