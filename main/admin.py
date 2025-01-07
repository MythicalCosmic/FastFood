from django.contrib import admin
from .models import *




admin.site.register(IngridientInvoiceItem)
admin.site.register(IngridientInvoice)
admin.site.register(Stock)
admin.site.register(StockMovement)