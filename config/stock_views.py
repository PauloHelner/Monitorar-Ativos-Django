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
        self.change_percent = 100.0 * float(data["regularMarketChangePercent"])


def home(request):
    ativos_list = []
    saved_list = []
    if request.user.is_authenticated:
        api_request = requests.get("https://brapi.dev/api/available")
        saved_tickers = Stock.objects.filter(owner=request.user)
        try:
            for element in saved_tickers:
                update_data = yq.Ticker(str(element)).price
                updated = Ativo(str(element), update_data[str(element)])
                saved_list.append(updated)
        except Exception as e:
            api = "error"
        try:
            api = json.loads(api_request.content)
            ticker_list = []
            for element in api["stocks"]:
                ticker_list.append(element + ".SA")
            for index in range(10):
                new_data = yq.Ticker(ticker_list[index]).price
                ativo = Ativo(ticker_list[index], new_data[ticker_list[index]])
                ativos_list.append(ativo)
        except Exception as e:
            api = "error"
    return render(request, "home.html", {"api": ativos_list, "saved": saved_list})


def add_stock(request, saved_ticker):
    if request.user.is_authenticated:
        try:
            Stock.objects.create(ticker=saved_ticker, owner=request.user)
        except Exception as e:
            print(e)
        return redirect("home")
