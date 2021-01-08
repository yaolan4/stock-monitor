import requests
import json
import seaborn as sns
import matplotlib.pyplot as plt, mpld3
import pandas as pd
from datetime import datetime
from matplotlib import rcParams

RAPIDAPI_KEY  = "9a415382damsh6fcebf2ec9284c2p1f2919jsn46e2378f8dca"
RAPIDAPI_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"

symbol_string = ""
inputdata = {}

def fetchStockData(symbol):
  
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"

    querystring = {"interval":"5m","symbol":symbol,"range":"5d","region":"US"}

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
    dt = datetime.fromtimestamp(ts)
    calendertime.append(dt.strftime("%m/%d/%Y"))

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

def get_stock_chart():
  try:
    retdata = fetchStockData('TSLA.MI')

    if (None != inputdata): 

      inputdata["Timestamp"] = parseTimestamp(retdata)

      inputdata["Values"] = parseValues(retdata)

      inputdata["Events"] = attachEvents(retdata)

      df = pd.DataFrame(inputdata)
      print(df)
      fig =  plt.figure()
      sns.set(style="darkgrid")

      rcParams['figure.figsize'] = 13,5
      rcParams['figure.subplot.bottom'] = 0.2

      ax = sns.lineplot(x="Timestamp", y="Values", hue="Events",dashes=False, markers=True, 
                  data=df, sort=False)
      
      ax.set_title('Symbol: ' + 'TSLA.MI')
      
      plt.xticks(
          rotation=45, 
          horizontalalignment='right',
          fontweight='light',
          fontsize='xx-small'  
      )
      #print(mpld3.fig_to_html(fig))
      #html_graph = mpld3.fig_to_html(fig)
      #plt.close(fig)
      #return html_graph
      plt.show()

  except Exception as e:
    print("Error")
    print(e)


get_stock_chart()