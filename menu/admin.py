from django.contrib import admin
from .models import Category, Dish, Deal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount_percent", "final_price",
                     "quantity_available", "is_active", "is_featured")
    list_editable = ("price", "discount_percent", "quantity_available", "is_active", "is_featured")
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("name", "description")

    def final_price(self, obj):
        return f"${obj.final_price}"


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("title", "deal_price", "is_active", "valid_from", "valid_until")
    list_editable = ("deal_price", "is_active")
    filter_horizontal = ("dishes",)
