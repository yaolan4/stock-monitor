from django.contrib import admin
from .models import Stock, StockChart, StockSummary
# Register your models here.

admin.site.register(Stock)
admin.site.register(StockChart)
admin.site.register(StockSummary)