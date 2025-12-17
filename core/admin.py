# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, TaxRecord


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")


@admin.register(TaxRecord)
class TaxRecordAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tax_year",
        "annual_gross_income",
        "allowable_deductions",
        "net_taxable_income",
        "annual_tax_due",
        "effective_tax_rate",
        "is_active",
        "created_at",
    )
    list_filter = ("tax_year", "is_active", "created_at", "tax_bracket")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = (
        "net_taxable_income",
        "annual_tax_due",
        "effective_tax_rate",
        "tax_bracket",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        ("User Information", {"fields": ("user", "tax_year", "is_active")}),
        ("Income Details", {"fields": ("annual_gross_income", "allowable_deductions")}),
        (
            "Computed Tax",
            {
                "fields": (
                    "net_taxable_income",
                    "annual_tax_due",
                    "effective_tax_rate",
                    "tax_bracket",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ("user",)
        return self.readonly_fields


# Unregister the original User admin and register the new one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Customize admin site header
admin.site.site_header = "Tax Calculator Administration"
admin.site.site_title = "Tax Calculator Admin"
admin.site.index_title = "Welcome to Tax Calculator Admin Portal"
