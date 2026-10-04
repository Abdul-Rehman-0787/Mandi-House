from django.contrib import admin
from .models import OpeningHours, TableBooking


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ("day_of_week", "is_open", "open_time", "close_time", "last_seating_time")
    list_editable = ("is_open", "open_time", "close_time", "last_seating_time")


@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "customer_phone", "party_size", "booking_date", "booking_time", "status")
    list_editable = ("status",)
    list_filter = ("status", "booking_date")
