import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from menu.models import Dish, Deal, Category

# Lightweight rule-based assistant. No external API key required, so the
# chatbot works fully offline / on localhost with zero setup. It can be
# swapped later for a real LLM API call (see README) without changing the
# frontend widget.

GREETINGS = ("hi", "hello", "hey", "salam", "assalam")


def _menu_summary():
    cats = Category.objects.prefetch_related("dishes")
    lines = []
    for c in cats:
        names = [d.name for d in c.dishes.filter(is_active=True)][:5]
        if names:
            lines.append(f"{c.name}: " + ", ".join(names))
    return lines


@csrf_protect
@require_POST
def chat_api(request):
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"reply": "Sorry, I couldn't read that message."}, status=400)

    message = (data.get("message") or "").strip().lower()[:500]
    if not message:
        return JsonResponse({"reply": "Please type a message."}, status=400)

    reply = _generate_reply(message)
    return JsonResponse({"reply": reply})


def _generate_reply(message):
    if any(g in message for g in GREETINGS):
        return (f"Hello! Welcome to {settings.RESTAURANT_NAME} 🍛. "
                f"I can help with our menu, deals, order status, or opening hours. What would you like to know?")

    if "hour" in message or "open" in message or "time" in message:
        return "We're open daily from 11:00 AM to 11:00 PM (Sydney time)."

    if "deal" in message or "discount" in message or "offer" in message:
        deals = [d for d in Deal.objects.filter(is_active=True) if d.is_currently_valid]
        if deals:
            names = ", ".join(d.title for d in deals[:5])
            return f"Current deals: {names}. Check the Deals page for full details!"
        return "We don't have any active deals right now, but check back soon!"

    if "menu" in message or "dish" in message or "food" in message:
        lines = _menu_summary()
        if lines:
            return "Here's a taste of our menu — " + " | ".join(lines)
        return "Our menu is being updated — please check the Menu page shortly."

    if "price" in message or "cost" in message or "$" in message:
        return "Prices are shown on each dish card in AUD ($). Deals may offer a bundled price."

    if "order" in message and ("status" in message or "confirm" in message):
        return ("Once you place an order, our team will call you on the phone number you provided "
                "to confirm it. No online payment is needed — you simply pay when you pick it up.")

    if "delivery" in message:
        return "We currently only offer takeaway (pickup). Delivery isn't available yet."

    if "pay" in message or "payment" in message:
        return "Payment is on pickup (cash or card in-store). Online payment isn't enabled yet."

    if "contact" in message or "phone" in message or "call" in message:
        return f"You can reach us at {settings.RESTAURANT_PHONE}."

    if "thank" in message:
        return "You're most welcome! Anything else I can help with?"

    return ("I'm not totally sure about that one — try asking about our menu, deals, "
            "opening hours, or how ordering works. You can also call us directly.")
