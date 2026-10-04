from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "customer_phone", "notes"]
        widgets = {
            "customer_name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Your full name", "autofocus": True, "maxlength": 120,
            }),
            "customer_phone": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "+61 4xx xxx xxx",
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control", "rows": 3, "placeholder": "Any special requests? (optional)",
            }),
        }

    def clean_customer_name(self):
        name = self.cleaned_data["customer_name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name
