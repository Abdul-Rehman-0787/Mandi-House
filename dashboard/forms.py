from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from menu.models import Dish, Category, Deal
from bookings.models import OpeningHours


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["category", "name", "description", "image", "price",
                  "discount_percent", "quantity_available", "is_active", "is_featured"]
        widgets = {
            "category": forms.Select(attrs={"class": "big-input"}),
            "name": forms.TextInput(attrs={"class": "big-input", "placeholder": "e.g. Chicken Mandi"}),
            "description": forms.Textarea(attrs={"class": "big-input", "rows": 3}),
            "price": forms.NumberInput(attrs={"class": "big-input", "step": "0.01", "min": "0"}),
            "discount_percent": forms.NumberInput(attrs={"class": "big-input", "min": "0", "max": "100"}),
            "quantity_available": forms.NumberInput(attrs={"class": "big-input", "min": "0"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "big-input"}),
            "order": forms.NumberInput(attrs={"class": "big-input"}),
        }


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ["title", "description", "image", "dishes", "deal_price", "is_active", "valid_until"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "big-input"}),
            "description": forms.Textarea(attrs={"class": "big-input", "rows": 3}),
            "deal_price": forms.NumberInput(attrs={"class": "big-input", "step": "0.01", "min": "0"}),
            "dishes": forms.CheckboxSelectMultiple(),
            "valid_until": forms.DateTimeInput(attrs={"class": "big-input", "type": "datetime-local"}),
        }


class StaffCreateForm(forms.Form):
    """Simple, friendly form the owner uses to create a staff login.
    No technical Django-admin knowledge required."""
    full_name = forms.CharField(
        label="Staff member's name", max_length=150,
        widget=forms.TextInput(attrs={"class": "big-input", "placeholder": "e.g. Sara Khan"}),
    )
    username = forms.CharField(
        label="Login ID", max_length=150,
        help_text="What the staff member will type in to log in. No spaces.",
        widget=forms.TextInput(attrs={"class": "big-input", "placeholder": "e.g. sara.k"}),
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "big-input"}),
        help_text="At least 8 characters. Share this with the staff member privately.",
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip().replace(" ", "")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("That login ID is already taken. Please choose another.")
        return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ["is_open", "open_time", "close_time", "last_seating_time"]
        widgets = {
            "open_time": forms.TimeInput(attrs={"class": "big-input", "type": "time"}),
            "close_time": forms.TimeInput(attrs={"class": "big-input", "type": "time"}),
            "last_seating_time": forms.TimeInput(attrs={"class": "big-input", "type": "time"}),
        }


OpeningHoursFormSet = forms.modelformset_factory(
    OpeningHours, form=OpeningHoursForm, extra=0
)
