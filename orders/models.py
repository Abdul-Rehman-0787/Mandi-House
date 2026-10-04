from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from menu.models import Dish, Deal

phone_validator = RegexValidator(
    regex=r"^\+?[0-9\s\-]{7,20}$",
    message="Enter a valid phone number, e.g. +61 400 000 000",
)


class Order(models.Model):
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
    customer_email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, help_text="Any special requests from the customer.")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING)
    is_takeaway = models.BooleanField(default=True, help_text="Pay-on-pickup takeaway order.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"

    @property
    def total(self):
        return sum((item.line_total for item in self.items.all()), 0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=150, help_text="Snapshot of the name at order time.")
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.item_name}"
