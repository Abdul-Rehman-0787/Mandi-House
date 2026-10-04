from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("django-admin/", admin.site.urls),  # low-level Django admin (superuser only)
    path("staff/", include("dashboard.urls")),  # friendly staff dashboard
    path("orders/", include("orders.urls")),
    path("bookings/", include("bookings.urls")),
    path("chatbot/", include("chatbot.urls")),
    path("", include("menu.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
