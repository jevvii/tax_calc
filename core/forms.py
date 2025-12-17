# core/forms.py
from django import forms
from .models import TaxRecord
from decimal import Decimal


class TaxInputForm(forms.ModelForm):
    """Form for tax input"""

    class Meta:
        model = TaxRecord
        fields = ["annual_gross_income", "allowable_deductions", "tax_year"]
        widgets = {
            "annual_gross_income": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "allowable_deductions": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "tax_year": forms.NumberInput(
                attrs={"class": "form-input", "min": "2023", "value": "2023"}
            ),
        }
        labels = {
            "annual_gross_income": "Annual Gross Income (PHP)",
            "allowable_deductions": "Allowable Deductions (PHP)",
            "tax_year": "Tax Year",
        }

    def clean_annual_gross_income(self):
        income = self.cleaned_data.get("annual_gross_income")
        if income and income < 0:
            raise forms.ValidationError("Income cannot be negative.")
        return income

    def clean_allowable_deductions(self):
        deductions = self.cleaned_data.get("allowable_deductions")
        if deductions and deductions < 0:
            raise forms.ValidationError("Deductions cannot be negative.")
        return deductions

    def clean(self):
        cleaned_data = super().clean()
        income = cleaned_data.get("annual_gross_income")
        deductions = cleaned_data.get("allowable_deductions")

        if income and deductions and deductions > income:
            raise forms.ValidationError(
                "Allowable deductions cannot exceed gross income."
            )

        return cleaned_data
