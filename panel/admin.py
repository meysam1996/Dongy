from django.contrib import admin
from panel.models import Invoice, People, Transaction

# Register your models here.

admin.site.register(Invoice)
admin.site.register(People)
admin.site.register(Transaction)
