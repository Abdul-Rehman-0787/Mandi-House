from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu_list, name="menu_list"),
    path("dish/<int:pk>/", views.dish_detail, name="dish_detail"),
    path("deals/", views.deals_list, name="deals_list"),
    path("about/", views.about, name="about"),
]
