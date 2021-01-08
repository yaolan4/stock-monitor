import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Stock (models.Model):
    stock_name = models.CharField(max_length=400)
    symbol= models.CharField(max_length=400, default='')

    def __str__(self) -> str:
        return self.stock_name

class StockSummary(models.Model):
    stock_name = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stock_long_business_summary = models.CharField(max_length=100000000000000)
    stock_pub_date = models.DateTimeField('date published')
    stock_profit_margins = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.stock_long_business_summary

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=365)

class StockChart(models.Model):
    stock_name = models.ForeignKey(Stock, on_delete=models.CASCADE)
    #stock_chart = 

    def __str__(self) -> str:
        return self.stock_name

