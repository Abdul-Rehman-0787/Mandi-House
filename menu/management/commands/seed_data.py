from django.core.management.base import BaseCommand
from menu.models import Category, Dish, Deal


class Command(BaseCommand):
    help = "Seeds the database with sample Mandi 1 menu data for demoing/testing."

    def handle(self, *args, **options):
        cats = {}
        for i, name in enumerate(["Mandi Plates", "Grills", "Rice & Sides", "Beverages", "Desserts"]):
            cat, _ = Category.objects.get_or_create(name=name, defaults={"order": i})
            cats[name] = cat

        dishes_data = [
            ("Mandi Plates", "Chicken Mandi", "Slow-cooked chicken over fragrant spiced rice.", 16.90, 0, 40, True),
            ("Mandi Plates", "Lamb Mandi", "Tender lamb, oven-roasted, served with basmati rice.", 21.90, 10, 25, True),
            ("Mandi Plates", "Beef Mandi", "Rich beef mandi with traditional Yemeni spices.", 19.90, 0, 30, False),
            ("Grills", "Mixed Grill Platter", "Chicken tikka, kofta and lamb chops.", 24.90, 0, 20, True),
            ("Grills", "Chicken Tikka", "Charcoal-grilled marinated chicken skewers.", 14.90, 0, 35, False),
            ("Rice & Sides", "Saffron Rice", "Fragrant basmati rice with saffron.", 6.50, 0, 50, False),
            ("Rice & Sides", "Garlic Sauce", "Creamy garlic sauce, a mandi essential.", 2.50, 0, 100, False),
            ("Beverages", "Mint Lemonade", "Refreshing housemade mint lemonade.", 5.50, 0, 60, False),
            ("Beverages", "Karak Chai", "Spiced milk tea, brewed the traditional way.", 4.50, 0, 60, False),
            ("Desserts", "Baklava (3pcs)", "Crispy, nutty, honey-soaked pastry.", 7.90, 0, 30, True),
        ]
        for cat_name, name, desc, price, disc, qty, featured in dishes_data:
            Dish.objects.get_or_create(
                name=name,
                defaults=dict(
                    category=cats[cat_name], description=desc, price=price,
                    discount_percent=disc, quantity_available=qty, is_featured=featured,
                ),
            )

        chicken = Dish.objects.get(name="Chicken Mandi")
        lemonade = Dish.objects.get(name="Mint Lemonade")
        deal, created = Deal.objects.get_or_create(
            title="Family Feast: 2 Chicken Mandi + 2 Drinks",
            defaults={"description": "Perfect for two! Two chicken mandi plates with two mint lemonades.",
                      "deal_price": 39.90},
        )
        if created:
            deal.dishes.set([chicken, lemonade])

        self.stdout.write(self.style.SUCCESS("Sample menu data seeded successfully."))
