from .cart import Cart


def cart_summary(request):
    """Makes cart item count available in every template (e.g. navbar badge)."""
    try:
        cart = Cart(request)
        return {"cart_item_count": len(cart)}
    except Exception:
        return {"cart_item_count": 0}
