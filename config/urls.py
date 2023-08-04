from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import stock_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # new
    path("accounts/", include("django.contrib.auth.urls")),
    path("", stock_views.home, name="home"),
    path("monitor/<monitor_ticker>", stock_views.monitor_stock, name="monitor"),
    path("edit/<edit_ticker>", stock_views.edit_stock, name="edit"),
    path("remove/<remove_ticker>", stock_views.remove_stock, name="remove"),
    path("add/<saved_ticker>", stock_views.add_stock, name="add"),
    path("exit", stock_views.logout, name="exit"),
]
