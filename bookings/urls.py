from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("reserve/", views.reserve_table, name="reserve_table"),
    path("reserve/success/<int:pk>/", views.booking_success, name="booking_success"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
]
