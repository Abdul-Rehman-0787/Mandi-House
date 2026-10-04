from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.staff_login, name="login"),          # staff-only login (give this URL to staff)
    path("owner-login/", views.owner_login, name="owner_login"),  # owner-only login (keep this one private)
    path("logout/", views.staff_logout, name="logout"),
    path("", views.home, name="home"),

    path("orders/", views.orders_list, name="orders_list"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("orders/<int:pk>/status/<str:new_status>/", views.order_set_status, name="order_set_status"),

    path("dishes/", views.dishes_list, name="dishes_list"),
    path("dishes/add/", views.dish_add, name="dish_add"),
    path("dishes/<int:pk>/edit/", views.dish_edit, name="dish_edit"),
    path("dishes/<int:pk>/delete/", views.dish_delete, name="dish_delete"),

    path("categories/", views.categories_list, name="categories_list"),

    path("deals/", views.deals_list, name="deals_list"),
    path("deals/add/", views.deal_add, name="deal_add"),
    path("deals/<int:pk>/edit/", views.deal_edit, name="deal_edit"),
    path("deals/<int:pk>/delete/", views.deal_delete, name="deal_delete"),

    path("staff/", views.staff_list, name="staff_list"),
    path("staff/add/", views.staff_add, name="staff_add"),
    path("staff/<int:pk>/toggle/", views.staff_toggle_active, name="staff_toggle_active"),
    path("staff/<int:pk>/delete/", views.staff_delete, name="staff_delete"),

    path("bookings/", views.bookings_list, name="bookings_list"),
    path("bookings/<int:pk>/", views.booking_detail, name="booking_detail"),
    path("bookings/<int:pk>/status/<str:new_status>/", views.booking_set_status, name="booking_set_status"),

    path("opening-hours/", views.opening_hours, name="opening_hours"),
]
