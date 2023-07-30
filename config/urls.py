from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import stock_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # new
    path("accounts/", include("django.contrib.auth.urls")),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path("", stock_views.home, name="home"),
    path("add/<saved_ticker>", stock_views.add_stock, name="add"),
]
