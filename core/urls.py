# core/urls.py
from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    DashboardView,
    TaxInputView,
    delete_tax_record,
)

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("tax-input/", TaxInputView.as_view(), name="tax_input"),
    path("delete-record/<int:pk>/", delete_tax_record, name="delete_record"),
]


# tax_calculator/urls.py (Main URLs)
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard')),
    path('', include('core.urls')),
]
"""
