from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import OpeningHours, TableBooking, DAY_CHOICES
from .forms import TableBookingForm

MY_BOOKINGS_SESSION_KEY = "my_booking_ids"


def reserve_table(request):
    # Make sure every weekday has an OpeningHours row so the schedule always
    # displays something sensible even before the owner customises it.
    existing_days = set(OpeningHours.objects.values_list("day_of_week", flat=True))
    for day_value, _ in DAY_CHOICES:
        if day_value not in existing_days:
            is_closed = day_value == 0  # default: closed Monday
            OpeningHours.objects.create(day_of_week=day_value, is_open=not is_closed)

    schedule = OpeningHours.objects.all()

    if request.method == "POST":
        form = TableBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            ids = request.session.get(MY_BOOKINGS_SESSION_KEY, [])
            ids.append(booking.pk)
            request.session[MY_BOOKINGS_SESSION_KEY] = ids
            request.session.modified = True
            return redirect("bookings:booking_success", pk=booking.pk)
    else:
        form = TableBookingForm()

    return render(request, "bookings/reserve_table.html", {"form": form, "schedule": schedule})


def booking_success(request, pk):
    booking = get_object_or_404(TableBooking, pk=pk)
    return render(request, "bookings/booking_success.html", {"booking": booking})


def my_bookings(request):
    ids = request.session.get(MY_BOOKINGS_SESSION_KEY, [])
    bookings = TableBooking.objects.filter(pk__in=ids).order_by("-created_at")

    phone_lookup_results = None
    phone = request.GET.get("phone", "").strip()
    if phone:
        phone_lookup_results = TableBooking.objects.filter(customer_phone__icontains=phone).order_by("-created_at")[:20]

    return render(request, "bookings/my_bookings.html", {
        "bookings": bookings, "phone": phone, "phone_lookup_results": phone_lookup_results,
    })
