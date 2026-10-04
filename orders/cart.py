"""
Simple session-based shopping cart.
Stored as: request.session['cart'] = {"dish_<id>": {"name":..,"price":..,"qty":..}, "deal_<id>": {...}}
Kept intentionally simple (no external deps) and defensive against tampering:
every price is re-validated against the database at checkout time, never
trusted from the session alone.
"""
from decimal import Decimal
from menu.models import Dish, Deal

SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_KEY)
        if cart is None:
            cart = {}
            self.session[SESSION_KEY] = cart
        self.cart = cart

    def _key(self, kind, obj_id):
        return f"{kind}_{obj_id}"

    def add(self, kind, obj_id, quantity=1):
        key = self._key(kind, obj_id)
        if key in self.cart:
            self.cart[key]["qty"] += quantity
        else:
            if kind == "dish":
                obj = Dish.objects.filter(pk=obj_id, is_active=True).first()
                if not obj:
                    return
                price = float(obj.final_price)
                name = obj.name
            else:
                obj = Deal.objects.filter(pk=obj_id, is_active=True).first()
                if not obj:
                    return
                price = float(obj.deal_price)
                name = obj.title
            self.cart[key] = {"kind": kind, "id": obj_id, "name": name, "price": price, "qty": quantity}
        self.save()

    def update(self, kind, obj_id, quantity):
        key = self._key(kind, obj_id)
        if key in self.cart:
            if quantity <= 0:
                del self.cart[key]
            else:
                self.cart[key]["qty"] = quantity
            self.save()

    def remove(self, kind, obj_id):
        key = self._key(kind, obj_id)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def clear(self):
        self.cart = {}
        self.session[SESSION_KEY] = {}
        self.save()

    def save(self):
        self.session[SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        for item in self.cart.values():
            yield item

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    @property
    def total(self):
        return round(sum(Decimal(str(item["price"])) * item["qty"] for item in self.cart.values()), 2)

    @property
    def is_empty(self):
        return len(self.cart) == 0
