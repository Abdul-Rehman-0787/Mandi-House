from django.conf import settings


def site_settings(request):
    """Makes restaurant-wide settings available in every template (e.g. footer)."""
    return {
        "RESTAURANT_NAME": settings.RESTAURANT_NAME,
        "RESTAURANT_PHONE": settings.RESTAURANT_PHONE,
        "RESTAURANT_ADDRESS": settings.RESTAURANT_ADDRESS,
    }
