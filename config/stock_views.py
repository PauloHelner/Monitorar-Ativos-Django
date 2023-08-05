from django.urls import reverse_lazy
from django.views import generic

from django.shortcuts import render, redirect
from accounts.models import Stock
from django.contrib import messages
from django.core.mail import send_mail

import requests
import json
import yahooquery as yq
import threading
import time
import copy

#   código global (not views)---------------------------------------------

THREADLESS = True
THREAD_LIST = {}


class Monitoring_Thread(threading.Thread):
    def __init__(self, user, stock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.stock = stock
        self.killing = False
        self.daemon = True
        self.start()

    def kill(self):
        self.killing = True

    def killed(self):
        return self.killing

    def run(self):
        period = copy.copy(self.stock.period)
        while (not self.killing) and (period == self.stock.period):
            data = yq.Ticker(self.stock.ticker).price
            if data[self.stock.ticker]["regularMarketPrice"] >= self.stock.top:
                send_mail(
                    "Alerta de Venda",
                    "O seu ativo de código "
                    + str(self.stock.ticker)
                    + " ultrapassou a cotação limite de R$ "
                    + str("%.2f" % self.stock.top)
                    + "\nA cotação atual é de R$ "
                    + str("%.2f" % data[self.stock.ticker]["regularMarketPrice"]),
                    "sistema@monitoramento.com",
                    [self.user.email],
                    fail_silently=False,
                )
            if data[self.stock.ticker]["regularMarketPrice"] <= self.stock.bottom:
                send_mail(
                    "Alerta de Compra",
                    "O seu ativo de código "
                    + str(self.stock.ticker)
                    + " está abaixo da cotação limite de R$ "
                    + str("%.2f" % self.stock.bottom)
                    + "\nA cotação atual é de R$ "
                    + str("%.2f" % data[self.stock.ticker]["regularMarketPrice"]),
                    "sistema@monitoramento.com",
                    [self.user.email],
                    fail_silently=False,
                )
            time.sleep(60 * period)
            try:
                self.stock = Stock.objects.get(
                    ticker=self.stock.ticker, owner=self.user
                )
            except Exception as e:
                break


def new_thread(user, stock):
    global THREAD_LIST
    THREAD_LIST[str(user) + str(stock)] = Monitoring_Thread(user, stock)


def delete_thread(user, stock):
    THREAD_LIST[str(user) + str(stock)].kill()


def first_threads(user, stocks):
    for stock in stocks:
        new_thread(user, stock)


class Ativo:
    def __init__(self, ticker, data):
        self.ticker = str(ticker)
        self.name = str(data["longName"])
        self.currency_symbol = str(data["currencySymbol"])
        self.previous_close = float(data["regularMarketPreviousClose"])
        self.open = float(data["regularMarketOpen"])
        self.price = float(data["regularMarketPrice"])
        self.change_percent = 100.0 * float(data["regularMarketChangePercent"])


#   fim do código global -------------------------------------------------------


def home(request, num=1):
    global THREADLESS
    ativos_list = []
    saved_list = []
    ticker_list = []
    if request.user.is_authenticated:
        api_request = requests.get("https://brapi.dev/api/available")
        saved_tickers = Stock.objects.filter(owner=request.user)
        if THREADLESS:
            first_threads(request.user, saved_tickers)
            THREADLESS = False
        try:
            for element in saved_tickers:
                update_data = yq.Ticker(str(element)).price
                updated = Ativo(str(element), update_data[str(element)])
                saved_list.append(updated)
        except Exception as e:
            api = "error"
        try:
            api = json.loads(api_request.content)
            for element in api["stocks"]:
                ticker_list.append(element + ".SA")
            page_offset = 10 * (int(num) - 1)
            for index in range(10):
                if (index + page_offset) < len(ticker_list):
                    new_data = yq.Ticker(ticker_list[index + page_offset]).price
                    ativo = Ativo(
                        ticker_list[index + page_offset],
                        new_data[ticker_list[index + page_offset]],
                    )
                    ativos_list.append(ativo)
            ticker_list.sort()
        except Exception as e:
            api = "error"
    return render(
        request,
        "home.html",
        {
            "api": ativos_list,
            "saved": saved_list,
            "pag": num,
            "total_pag": int(len(ticker_list) / 10) + (len(ticker_list) % 10 > 0),
            "ticker_list": ticker_list,
        },
    )


def home_pag(request, num):
    return home(request, num)


def add_stock(request, saved_ticker):
    if request.user.is_authenticated:
        try:
            stock = Stock.objects.create(ticker=saved_ticker, owner=request.user)
            new_thread(request.user, stock)
        except Exception as e:
            print(e)
    return redirect("home")


def monitor_stock(request, monitor_ticker):
    if request.user.is_authenticated:
        saved = []
        fetched = []
        try:
            saved = Stock.objects.get(ticker=monitor_ticker, owner=request.user)
            fetched = yq.Ticker(monitor_ticker).price
        except Exception as e:
            print(e)
        data = Ativo(str(monitor_ticker), fetched[monitor_ticker])
        saved_data = saved.get_data()
        return render(request, "monitor.html", {"saved_data": saved_data, "data": data})
    return redirect("home")


def edit_stock(request, edit_ticker):
    if request.user.is_authenticated:
        try:
            info = Stock.objects.get(ticker=edit_ticker, owner=request.user)
            info.top = float(request.POST["top"])
            info.bottom = float(request.POST["bottom"])
            old_period = copy.copy(info.period)
            info.period = int(request.POST["period"])
            info.save()
            if old_period != info.period:
                new_thread(request.user, info)
        except Exception as e:
            print(e)
    return redirect("home")


def remove_stock(request, remove_ticker):
    if request.user.is_authenticated:
        try:
            info = Stock.objects.get(ticker=remove_ticker, owner=request.user)
            info.delete()
        except Exception as e:
            print(e)
    return redirect("home")


def logout(request):
    global THREADLESS
    global THREAD_LIST
    THREADLESS = True
    for thread in THREAD_LIST.values():
        thread.kill()
    return redirect("home")
