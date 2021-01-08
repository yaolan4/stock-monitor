import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

querystring = {"symbol":"TSLA.MI","region":"US"}

headers = {
    'x-rapidapi-key': "9a415382damsh6fcebf2ec9284c2p1f2919jsn46e2378f8dca",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)