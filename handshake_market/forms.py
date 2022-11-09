from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator


class CashInForm(forms.Form):
    amount = forms.DecimalField(label="Cash In Amount", max_digits=19, decimal_places=2, validators=[
        MinValueValidator(Decimal('50.00')),
    ])

    widget = {
        'amount': forms.NumberInput(attrs={
            'max': '1000',  # For maximum number
            'min': '10',  # For minimum number
        }),
    }


class PriceUpdateForm(forms.Form):
    amount = forms.DecimalField(label="New Price", max_digits=19, decimal_places=2, validators=[
        MinValueValidator(Decimal('5.00')),
    ])
