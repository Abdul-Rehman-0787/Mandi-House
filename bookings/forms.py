from django import forms
from django.utils import timezone
from .models import TableBooking, OpeningHours


class TableBookingForm(forms.ModelForm):
    class Meta:
        model = TableBooking
        fields = ["customer_name", "customer_phone", "party_size", "booking_date", "booking_time", "notes"]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}),
            "customer_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+61 4xx xxx xxx"}),
            "party_size": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 20}),
            "booking_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "booking_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3,
                                            "placeholder": "Any special requests? (optional)"}),
        }

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("booking_date")
        time_ = cleaned.get("booking_time")
        if date and time_:
            if date < timezone.localdate():
                raise forms.ValidationError("Please choose a date from today onward.")
            hours = OpeningHours.objects.filter(day_of_week=date.weekday()).first()
            if not hours or not hours.is_open:
                raise forms.ValidationError("We're closed that day — please pick another date.")
            if not (hours.open_time <= time_ <= hours.last_seating_time):
                raise forms.ValidationError(
                    f"That time is outside our seating hours for {hours.get_day_of_week_display()} "
                    f"({hours.open_time.strftime('%I:%M %p')} – {hours.last_seating_time.strftime('%I:%M %p')})."
                )
        return cleaned
