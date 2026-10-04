from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db import transaction
from menu.models import Dish, Deal
from .cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem

MY_ORDERS_SESSION_KEY = "my_order_ids"


@require_POST
def add_to_cart(request, kind, pk):
    if kind not in ("dish", "deal"):
        messages.error(request, "Invalid item.")
        return redirect("menu:menu_list")
    cart = Cart(request)
    qty = 1
    try:
        qty = max(1, int(request.POST.get("quantity", 1)))
    except (TypeError, ValueError):
        qty = 1
    cart.add(kind, pk, quantity=qty)
    messages.success(request, "Added to your cart.")
    return redirect(request.POST.get("next") or "orders:cart_detail")


@require_POST
def update_cart_item(request, kind, pk):
    cart = Cart(request)
    try:
        qty = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty = 1
    cart.update(kind, pk, qty)
    return redirect("orders:cart_detail")


@require_POST
def remove_from_cart(request, kind, pk):
    cart = Cart(request)
    cart.remove(kind, pk)
    messages.info(request, "Item removed from your cart.")
    return redirect("orders:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "orders/cart_detail.html", {"cart": cart})


def checkout(request):
    cart = Cart(request)
    if cart.is_empty:
        messages.warning(request, "Your cart is empty. Add some delicious mandi first!")
        return redirect("menu:menu_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.is_takeaway = True
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        dish_id=item["id"] if item["kind"] == "dish" else None,
                        deal_id=item["id"] if item["kind"] == "deal" else None,
                        item_name=item["name"],
                        unit_price=item["price"],
                        quantity=item["qty"],
                    )
            cart.clear()

            # Remember this order in the visitor's session so they can track
            # it later on the "My Orders" page without needing an account.
            my_orders = request.session.get(MY_ORDERS_SESSION_KEY, [])
            if order.pk not in my_orders:
                my_orders.append(order.pk)
            request.session[MY_ORDERS_SESSION_KEY] = my_orders
            request.session.modified = True

            return redirect("orders:order_success", pk=order.pk)
    else:
        form = CheckoutForm()

    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/order_success.html", {
        "order": order,
        "restaurant_phone": settings.RESTAURANT_PHONE,
    })


def my_orders(request):
    """
    Shows the orders placed from this browser (remembered in the session).
    If the person switched devices/browsers, they can look an order up by
    phone number instead — no account/login required either way.
    """
    order_ids = request.session.get(MY_ORDERS_SESSION_KEY, [])
    orders = Order.objects.filter(pk__in=order_ids).order_by("-created_at")

    phone_lookup_results = None
    phone = request.GET.get("phone", "").strip()
    if phone:
        phone_lookup_results = Order.objects.filter(customer_phone__icontains=phone).order_by("-created_at")[:20]

    return render(request, "orders/my_orders.html", {
        "orders": orders,
        "phone": phone,
        "phone_lookup_results": phone_lookup_results,
    })
