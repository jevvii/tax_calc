# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib import messages
from .models import TaxRecord
from .forms import TaxInputForm


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "core/register.html"
    success_url = reverse_lazy("login")


class CustomLoginView(LoginView):
    """Custom login view"""

    template_name = "core/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view"""

    next_page = "login"
    http_method_names = ["get", "post"]  # allow GET requests

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view displaying tax summary"""

    template_name = "core/dashboard.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the most recent active tax record
        tax_record = TaxRecord.objects.filter(
            user=self.request.user, is_active=True
        ).first()

        context["tax_record"] = tax_record
        context["has_tax_record"] = tax_record is not None

        # Get all tax records for history
        context["tax_history"] = TaxRecord.objects.filter(user=self.request.user)[
            :5
        ]  # Last 5 records

        return context


class TaxInputView(LoginRequiredMixin, CreateView):
    """View for inputting tax information"""

    model = TaxRecord
    form_class = TaxInputForm
    template_name = "core/tax_input.html"
    success_url = reverse_lazy("dashboard")
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Tax calculation completed successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


@login_required
def delete_tax_record(request, pk):
    """Delete a tax record"""
    try:
        record = TaxRecord.objects.get(pk=pk, user=request.user)
        record.delete()
        messages.success(request, "Tax record deleted successfully.")
    except TaxRecord.DoesNotExist:
        messages.error(request, "Tax record not found.")

    return redirect("dashboard")
