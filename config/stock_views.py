from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.shortcuts import render, redirect
from accounts.models import Stock
from django.contrib import messages

import requests
import json
import yahooquery as yq


class Ativo:
    def __init__(self, ticker, data):
        self.ticker = str(ticker)
        self.name = str(data["longName"])
        self.currency_symbol = str(data["currencySymbol"])
        self.previous_close = float(data["regularMarketPreviousClose"])
        self.open = float(data["regularMarketOpen"])
        self.price = float(data["regularMarketPrice"])
        self.change_percent = float(data["regularMarketChangePercent"])


def home(request):
    api_request = requests.get("https://brapi.dev/api/available")
    aapl = yq.Ticker("petr4.sa")

    try:
        api = json.loads(api_request.content)
        ticker_list = []
        ativos_list = []
        for element in api["stocks"]:
            ticker_list.append(element + ".SA")
        for index in range(10):
            # valid_ticker = str(
            #    yq.search(ticker, first_quote=True, country="Brazil")["symbol"]
            # )
            # yahoo_ticker_list.append(valid_ticker)
            new_data = yq.Ticker(ticker_list[index]).price
            print(new_data)
            ativo = Ativo(ticker_list[index], new_data[ticker_list[index]])
            ativos_list.append(ativo)

    except Exception as e:
        api = "error"
    return render(request, "home.html", {"api": ativos_list})


#    if request.method == "POST":
#        ticker = request.POST["ticker"]
#        api_request = requests.get("https://mfinance.com.br/api/v1/fiis/ALMI11")
#        try:
#            api = json.loads(api_request.content)
#        except Exception as e:
#            api = "error"
#        return render(request, "home.html", {"api": api})
#
#    else:
#        ticker = Stock.objects.all()
#        output = []
#        for ticker_item in ticker:
#            api_request = requests.get("https://mfinance.com.br/api/v1/fiis/ALMI11")
#            try:
#                api = json.loads(api_request.content)
#                output.append(api)
#            except Exception as e:
#                api = "error"
#        return render(
#            request, "home.html", {"ticker": "Ticker Does not exist", "output": output}
#        )
