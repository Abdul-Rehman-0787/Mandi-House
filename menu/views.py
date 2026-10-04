from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Category, Dish, Deal


def home(request):
    """Landing page: hero, featured dishes, active deals."""
    featured = Dish.objects.filter(is_active=True, is_featured=True)[:6]
    deals = [d for d in Deal.objects.filter(is_active=True) if d.is_currently_valid][:4]
    categories = Category.objects.all()
    return render(request, "menu/home.html", {
        "featured": featured,
        "deals": deals,
        "categories": categories,
    })


def menu_list(request):
    """Full menu, grouped by category, with optional category filter."""
    categories = Category.objects.prefetch_related("dishes")
    selected = request.GET.get("category")
    if selected:
        categories = categories.filter(id=selected)
    return render(request, "menu/menu_list.html", {
        "categories": categories,
        "all_categories": Category.objects.all(),
        "selected": selected,
    })


def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk, is_active=True)
    return render(request, "menu/dish_detail.html", {"dish": dish})


def deals_list(request):
    deals = [d for d in Deal.objects.filter(is_active=True) if d.is_currently_valid]
    return render(request, "menu/deals.html", {"deals": deals})


def about(request):
    return render(request, "menu/about.html", {})
