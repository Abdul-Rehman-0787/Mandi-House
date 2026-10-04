from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST

from menu.models import Dish, Category, Deal
from orders.models import Order
from bookings.models import TableBooking, OpeningHours
from .forms import DishForm, CategoryForm, DealForm, StaffCreateForm, OpeningHoursFormSet
from .decorators import owner_required, staff_or_owner_required


def owner_login(request):
    """Login page for the restaurant owner (superuser) only."""
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if not user.is_superuser:
            messages.error(request, "This login isn't an owner account. Please use the Staff Login page instead.")
        else:
            login(request, user)
            return redirect("dashboard:home")
    return render(request, "dashboard/owner_login.html", {"form": form})


def staff_login(request):
    """Login page for regular staff accounts only (not the owner)."""
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user.is_superuser:
            messages.error(request, "This is a staff-only login. Please use the Owner Login page instead.")
        elif not user.is_staff:
            messages.error(request, "This account does not have staff access.")
        else:
            login(request, user)
            return redirect("dashboard:home")
    return render(request, "dashboard/login.html", {"form": form})


@login_required
def staff_logout(request):
    logout(request)
    return redirect("menu:home")


@staff_or_owner_required
def home(request):
    pending_orders = Order.objects.filter(status=Order.STATUS_PENDING).count()
    pending_bookings = TableBooking.objects.filter(status=TableBooking.STATUS_PENDING).count()
    total_dishes = Dish.objects.count()
    out_of_stock = Dish.objects.filter(quantity_available=0).count()
    active_deals = Deal.objects.filter(is_active=True).count()
    recent_orders = Order.objects.all()[:8]
    return render(request, "dashboard/home.html", {
        "pending_orders": pending_orders,
        "pending_bookings": pending_bookings,
        "total_dishes": total_dishes,
        "out_of_stock": out_of_stock,
        "active_deals": active_deals,
        "recent_orders": recent_orders,
    })


# --------------------------- ORDERS ---------------------------------------
@staff_or_owner_required
def orders_list(request):
    status = request.GET.get("status")
    orders = Order.objects.all()
    if status:
        orders = orders.filter(status=status)
    return render(request, "dashboard/orders_list.html", {
        "orders": orders, "status": status, "statuses": Order.STATUS_CHOICES,
    })


@staff_or_owner_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "dashboard/order_detail.html", {"order": order})


@staff_or_owner_required
@require_POST
def order_set_status(request, pk, new_status):
    order = get_object_or_404(Order, pk=pk)
    valid = dict(Order.STATUS_CHOICES)
    if new_status in valid:
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.pk} marked as {valid[new_status]}.")
    return redirect("dashboard:order_detail", pk=pk)


# --------------------------- DISHES ----------------------------------------
@owner_required
def dishes_list(request):
    dishes = Dish.objects.select_related("category").all()
    return render(request, "dashboard/dishes_list.html", {"dishes": dishes})


@owner_required
def dish_add(request):
    form = DishForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New dish added to the menu!")
        return redirect("dashboard:dishes_list")
    return render(request, "dashboard/dish_form.html", {"form": form, "title": "Add a New Dish"})


@owner_required
def dish_edit(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    form = DishForm(request.POST or None, request.FILES or None, instance=dish)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Dish updated!")
        return redirect("dashboard:dishes_list")
    return render(request, "dashboard/dish_form.html", {"form": form, "title": f"Edit: {dish.name}", "dish": dish})


@owner_required
@require_POST
def dish_delete(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    name = dish.name
    dish.delete()
    messages.success(request, f"'{name}' was removed from the menu.")
    return redirect("dashboard:dishes_list")


# --------------------------- CATEGORIES -------------------------------------
@owner_required
def categories_list(request):
    categories = Category.objects.all()
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category added!")
        return redirect("dashboard:categories_list")
    return render(request, "dashboard/categories_list.html", {"categories": categories, "form": form})


# --------------------------- DEALS ------------------------------------------
@owner_required
def deals_list(request):
    deals = Deal.objects.all()
    return render(request, "dashboard/deals_list.html", {"deals": deals})


@owner_required
def deal_add(request):
    form = DealForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New deal created!")
        return redirect("dashboard:deals_list")
    return render(request, "dashboard/deal_form.html", {"form": form, "title": "Add a New Deal"})


@owner_required
def deal_edit(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    form = DealForm(request.POST or None, request.FILES or None, instance=deal)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Deal updated!")
        return redirect("dashboard:deals_list")
    return render(request, "dashboard/deal_form.html", {"form": form, "title": f"Edit: {deal.title}"})


@owner_required
@require_POST
def deal_delete(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    deal.delete()
    messages.success(request, "Deal removed.")
    return redirect("dashboard:deals_list")


# --------------------------- STAFF ACCOUNTS (owner only) --------------------
@owner_required
def staff_list(request):
    staff_users = User.objects.filter(is_staff=True, is_superuser=False).order_by("username")
    return render(request, "dashboard/staff_list.html", {"staff_users": staff_users})


@owner_required
def staff_add(request):
    form = StaffCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["full_name"],
        )
        user.is_staff = True
        user.is_superuser = False
        user.save()
        messages.success(request, f"Staff login created for {form.cleaned_data['full_name']}.")
        return redirect("dashboard:staff_list")
    return render(request, "dashboard/staff_form.html", {"form": form})


@owner_required
@require_POST
def staff_toggle_active(request, pk):
    staff_user = get_object_or_404(User, pk=pk, is_superuser=False)
    staff_user.is_active = not staff_user.is_active
    staff_user.save()
    state = "enabled" if staff_user.is_active else "disabled"
    messages.success(request, f"Login for {staff_user.first_name or staff_user.username} was {state}.")
    return redirect("dashboard:staff_list")


@owner_required
@require_POST
def staff_delete(request, pk):
    staff_user = get_object_or_404(User, pk=pk, is_superuser=False)
    name = staff_user.first_name or staff_user.username
    staff_user.delete()
    messages.success(request, f"Removed staff login for {name}.")
    return redirect("dashboard:staff_list")


# --------------------------- TABLE BOOKINGS ---------------------------------
@staff_or_owner_required
def bookings_list(request):
    status = request.GET.get("status")
    bookings = TableBooking.objects.all()
    if status:
        bookings = bookings.filter(status=status)
    return render(request, "dashboard/bookings_list.html", {
        "bookings": bookings, "status": status, "statuses": TableBooking.STATUS_CHOICES,
    })


@staff_or_owner_required
def booking_detail(request, pk):
    booking = get_object_or_404(TableBooking, pk=pk)
    return render(request, "dashboard/booking_detail.html", {"booking": booking})


@staff_or_owner_required
@require_POST
def booking_set_status(request, pk, new_status):
    booking = get_object_or_404(TableBooking, pk=pk)
    valid = dict(TableBooking.STATUS_CHOICES)
    if new_status in valid:
        booking.status = new_status
        booking.save()
        messages.success(request, f"Booking #{booking.pk} marked as {valid[new_status]}.")
    return redirect("dashboard:booking_detail", pk=pk)


@owner_required
def opening_hours(request):
    # Ensure every day of the week has a row before showing the formset.
    from bookings.models import DAY_CHOICES
    existing_days = set(OpeningHours.objects.values_list("day_of_week", flat=True))
    for day_value, _ in DAY_CHOICES:
        if day_value not in existing_days:
            OpeningHours.objects.create(day_of_week=day_value, is_open=(day_value != 0))

    queryset = OpeningHours.objects.all().order_by("day_of_week")
    if request.method == "POST":
        formset = OpeningHoursFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Opening hours updated!")
            return redirect("dashboard:opening_hours")
    else:
        formset = OpeningHoursFormSet(queryset=queryset)

    days = dict(DAY_CHOICES)
    forms_with_days = list(zip([days[o.day_of_week] for o in queryset], formset.forms))
    return render(request, "dashboard/opening_hours.html", {
        "formset": formset, "forms_with_days": forms_with_days,
    })
