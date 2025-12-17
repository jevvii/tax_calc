# core/utils.py
from decimal import Decimal, ROUND_HALF_UP


def compute_tax(net_income):
    """
    Compute Philippine income tax based on TRAIN Law (Part 2, 2023 onwards)

    Tax Brackets:
    - ₱250,000 and below: 0%
    - Above ₱250,000 to ₱400,000: 15% of excess over ₱250,000
    - Above ₱400,000 to ₱800,000: ₱22,500 + 20% of excess over ₱400,000
    - Above ₱800,000 to ₱2,000,000: ₱102,500 + 25% of excess over ₱800,000
    - Above ₱2,000,000 to ₱8,000,000: ₱402,500 + 30% of excess over ₱2,000,000
    - Above ₱8,000,000: ₱2,202,500 + 35% of excess over ₱8,000,000

    Args:
        net_income (Decimal): Net taxable income

    Returns:
        dict: Contains annual_tax_due, effective_tax_rate, and tax_bracket
    """
    net_income = Decimal(str(net_income))

    # Tax brackets
    brackets = [
        {
            "limit": Decimal("250000"),
            "base": Decimal("0"),
            "rate": Decimal("0"),
            "excess_over": Decimal("0"),
        },
        {
            "limit": Decimal("400000"),
            "base": Decimal("0"),
            "rate": Decimal("0.15"),
            "excess_over": Decimal("250000"),
        },
        {
            "limit": Decimal("800000"),
            "base": Decimal("22500"),
            "rate": Decimal("0.20"),
            "excess_over": Decimal("400000"),
        },
        {
            "limit": Decimal("2000000"),
            "base": Decimal("102500"),
            "rate": Decimal("0.25"),
            "excess_over": Decimal("800000"),
        },
        {
            "limit": Decimal("8000000"),
            "base": Decimal("402500"),
            "rate": Decimal("0.30"),
            "excess_over": Decimal("2000000"),
        },
        {
            "limit": None,
            "base": Decimal("2202500"),
            "rate": Decimal("0.35"),
            "excess_over": Decimal("8000000"),
        },
    ]

    annual_tax_due = Decimal("0")
    tax_bracket = ""

    # Determine bracket and compute tax
    if net_income <= Decimal("250000"):
        annual_tax_due = Decimal("0")
        tax_bracket = "₱250,000 and below (0%)"
    elif net_income <= Decimal("400000"):
        excess = net_income - Decimal("250000")
        annual_tax_due = excess * Decimal("0.15")
        tax_bracket = "₱250,001 - ₱400,000 (15%)"
    elif net_income <= Decimal("800000"):
        excess = net_income - Decimal("400000")
        annual_tax_due = Decimal("22500") + (excess * Decimal("0.20"))
        tax_bracket = "₱400,001 - ₱800,000 (20%)"
    elif net_income <= Decimal("2000000"):
        excess = net_income - Decimal("800000")
        annual_tax_due = Decimal("102500") + (excess * Decimal("0.25"))
        tax_bracket = "₱800,001 - ₱2,000,000 (25%)"
    elif net_income <= Decimal("8000000"):
        excess = net_income - Decimal("2000000")
        annual_tax_due = Decimal("402500") + (excess * Decimal("0.30"))
        tax_bracket = "₱2,000,001 - ₱8,000,000 (30%)"
    else:
        excess = net_income - Decimal("8000000")
        annual_tax_due = Decimal("2202500") + (excess * Decimal("0.35"))
        tax_bracket = "Above ₱8,000,000 (35%)"

    # Round to 2 decimal places
    annual_tax_due = annual_tax_due.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Calculate effective tax rate
    if net_income > 0:
        effective_tax_rate = ((annual_tax_due / net_income) * 100).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    else:
        effective_tax_rate = Decimal("0.00")

    return {
        "annual_tax_due": annual_tax_due,
        "effective_tax_rate": effective_tax_rate,
        "tax_bracket": tax_bracket,
    }


def format_currency(amount):
    """Format amount as Philippine Peso"""
    return f"₱{amount:,.2f}"
