from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views
from . import stock_views
from accounts.forms import CustomAuthenticationForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # new
    path("accounts/", include("django.contrib.auth.urls")),
    path("", stock_views.home, name="home"),
    path(
        "login/",
        views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),
    path("pag/<num>", stock_views.home_pag, name="pag"),
    path("monitor/<monitor_ticker>", stock_views.monitor_stock, name="monitor"),
    path("edit/<edit_ticker>", stock_views.edit_stock, name="edit"),
    path("remove/<remove_ticker>", stock_views.remove_stock, name="remove"),
    path("add/<saved_ticker>", stock_views.add_stock, name="add"),
    path("exit", stock_views.logout, name="exit"),
]
