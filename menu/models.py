from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Category(models.Model):
    """Grouping for dishes, e.g. Mandi, Grills, Rice, Beverages."""
    name = models.CharField(max_length=80, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Dish(models.Model):
    """A single menu item the admin can fully manage."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="dishes/", blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)],
                                 help_text="Price in AUD ($).")
    discount_percent = models.PositiveIntegerField(
        default=0, help_text="0-100. Applied automatically to show a sale price."
    )
    quantity_available = models.PositiveIntegerField(
        default=50, help_text="Stock/servings left today. Set to 0 to mark as sold out."
    )
    is_active = models.BooleanField(default=True, help_text="Untick to hide this dish from the site.")
    is_featured = models.BooleanField(default=False, help_text="Show in the 'Chef's Picks' section.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category__order", "name"]

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.quantity_available > 0 and self.is_active

    @property
    def final_price(self):
        if self.discount_percent:
            discount = (self.price * self.discount_percent) / 100
            return round(self.price - discount, 2)
        return self.price

    @property
    def has_discount(self):
        return self.discount_percent > 0


class Deal(models.Model):
    """A combo/bundle deal, e.g. '2 Mandi Plates + Drinks for $25'."""
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="deals/", blank=True, null=True)
    dishes = models.ManyToManyField(Dish, related_name="deals", blank=True)
    deal_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-is_active", "-valid_from"]

    def __str__(self):
        return self.title

    @property
    def is_currently_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        return now >= self.valid_from
