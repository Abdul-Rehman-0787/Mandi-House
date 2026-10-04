from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<str:kind>/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<str:kind>/<int:pk>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<str:kind>/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/<int:pk>/", views.order_success, name="order_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
]
