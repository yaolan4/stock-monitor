from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
import requests
from django.template import loader

from .models import Stock, StockSummary, StockChart
import json
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
import seaborn as sns
import matplotlib.pyplot as plt
import mpld3
import pandas as pd
from datetime import datetime as dt
from matplotlib import rcParams
from django.template.loader import render_to_string

# Create your views here.
# global vars

RAPIDAPI_KEY  = "9a415382damsh6fcebf2ec9284c2p1f2919jsn46e2378f8dca"
RAPIDAPI_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"

symbol_string = ""
inputdata = {}

def index(request):
    try:
        stocks = Stock.objects.all()

    except Stock.DoesNotExist:
        raise Http404("Stock does not exist")
    context = {
        "stocks": stocks
    }
    return render(request, 'stockdashboard/index.html', context=context)

def detail(request):
    try: 
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
        
        #print(request.POST['stock'])
        requested_stock = get_object_or_404(Stock, stock_name=request.POST['stock'])
        #print(requested_stock.symbol)
        querystring = {"symbol":requested_stock.symbol,"region":"US"}

        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST}
        response = requests.request("GET", url, headers=headers, params=querystring)
        summary_obj = json.loads(response.text)
        print(requested_stock.stocksummary_set is None)
        # stock_obj = Stock.objects.get(id=1)
        if requested_stock.stocksummary_set.count() == 0: 
            stock_summary_obj = requested_stock.stocksummary_set.create(stock_long_business_summary=summary_obj['summaryProfile']['longBusinessSummary'],
                stock_pub_date=timezone.now(),
                stock_profit_margins=summary_obj['defaultKeyStatistics']['profitMargins']['raw'])
        else:
            stock_summary_obj = requested_stock.stocksummary_set.get()

        html_graph = get_stock_chart(requested_stock)
        context = {
            "stock_summary": stock_summary_obj.stock_long_business_summary,
            "stock_name" : requested_stock.stock_name,
            "stock_profit_margins" : stock_summary_obj.stock_profit_margins,
            "html_graph" : html_graph
        }
        
    except Stock.DoesNotExist:
        raise Http404("Stock does not exist.")
    except MultiValueDictKeyError:
        raise Http404("Please choose a stock.")

    
    # print(response.text)
    return render(request, 'stockdashboard/chart.html', context=context)

def fetchStockData(symbol):
  
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"

    querystring = {"interval":"1d","symbol":symbol,"range":"1y","region":"US"}

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    chart_obj = json.loads(response.text)
    return chart_obj



def parseTimestamp(inputdata):

  timestamplist = []

  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])

  calendertime = []

  for ts in timestamplist:
    dt_input = dt.fromtimestamp(ts)
    calendertime.append(dt_input.strftime("%m/%d/%Y"))

  return calendertime

def parseValues(inputdata):

  valueList = []
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])
  return valueList


def attachEvents(inputdata):

  eventlist = []

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventlist.append("open")  

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventlist.append("close")
  return eventlist

def get_stock_chart(requested_stock):
  html_graph = ''
  try:
    retdata = fetchStockData(requested_stock.symbol)

    if (None != inputdata): 

      inputdata["Timestamp"] = parseTimestamp(retdata)

      inputdata["Values"] = parseValues(retdata)

      inputdata["Events"] = attachEvents(retdata)

      df = pd.DataFrame(inputdata)
      #print(df)
      fig =  plt.figure()
      fig.set_size_inches(10.5, 6.5 , forward=True)
      dates = df['Timestamp']
      dates = [pd.to_datetime(d) for d in dates]
      plt.plot(dates, df['Values'], '-ok')

      plt.title('Symbol: ' + requested_stock.symbol)
      plt.ylabel("Stock Price")
      plt.xlabel("Date")
      #print(mpld3.fig_to_html(fig))
      html_graph = mpld3.fig_to_html(fig)


  except Exception as e:
    print("Error")
    print(e)
  return html_graph