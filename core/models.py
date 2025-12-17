# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class UserProfile(models.Model):
    """Extended user profile for additional user information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    tin = models.CharField(max_length=20, blank=True, null=True, verbose_name="TIN")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class TaxRecord(models.Model):
    """Model to store tax computation records"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tax_records")

    # Income Data
    annual_gross_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Annual gross income in PHP",
    )
    allowable_deductions = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
        help_text="Total allowable deductions in PHP",
    )

    # Computed Fields
    net_taxable_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        editable=False,
        help_text="Gross income minus deductions",
    )
    annual_tax_due = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        editable=False,
        help_text="Computed tax based on TRAIN Law",
    )
    effective_tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        editable=False,
        help_text="Effective tax rate as percentage",
    )
    tax_bracket = models.CharField(
        max_length=100, editable=False, help_text="Income tax bracket"
    )

    # Metadata
    tax_year = models.IntegerField(default=2023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Most recent record")

    def __str__(self):
        return (
            f"{self.user.username} - {self.tax_year} (₱{self.annual_gross_income:,.2f})"
        )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tax Record"
        verbose_name_plural = "Tax Records"
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):
        """Override save to compute tax before saving"""
        from .utils import compute_tax

        # Compute net taxable income
        self.net_taxable_income = self.annual_gross_income - self.allowable_deductions

        # Compute tax
        tax_result = compute_tax(self.net_taxable_income)
        self.annual_tax_due = tax_result["annual_tax_due"]
        self.effective_tax_rate = tax_result["effective_tax_rate"]
        self.tax_bracket = tax_result["tax_bracket"]

        # Set all other records for this user as inactive
        if self.is_active:
            TaxRecord.objects.filter(user=self.user, is_active=True).update(
                is_active=False
            )

        super().save(*args, **kwargs)
