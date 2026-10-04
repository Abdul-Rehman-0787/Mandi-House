from django.db import models
from django.core.validators import RegexValidator
from orders.models import phone_validator

DAY_CHOICES = [
    (0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"),
    (4, "Friday"), (5, "Saturday"), (6, "Sunday"),
]


class OpeningHours(models.Model):
    """
    Editable by the owner from the Staff Dashboard. Defines which days the
    restaurant is open, and generates the bookable time slots shown on the
    'Reserve a Table' page.
    """
    day_of_week = models.IntegerField(choices=DAY_CHOICES, unique=True)
    is_open = models.BooleanField(default=True)
    open_time = models.TimeField(default="17:30")
    close_time = models.TimeField(default="23:00")
    last_seating_time = models.TimeField(
        default="22:15", help_text="Last time a table booking can be made for that day."
    )

    class Meta:
        ordering = ["day_of_week"]
        verbose_name_plural = "Opening Hours"

    def __str__(self):
        return self.get_day_of_week_display()

    def slots(self, interval_minutes=30):
        """Generate bookable time slots between open_time and last_seating_time."""
        if not self.is_open:
            return []
        from datetime import datetime, timedelta
        slots = []
        current = datetime.combine(datetime.today(), self.open_time)
        end = datetime.combine(datetime.today(), self.last_seating_time)
        while current <= end:
            slots.append(current.time())
            current += timedelta(minutes=interval_minutes)
        return slots


class TableBooking(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending confirmation"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=20, validators=[phone_validator])
    party_size = models.PositiveIntegerField(default=2)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Table for {self.party_size} — {self.customer_name} ({self.booking_date})"
