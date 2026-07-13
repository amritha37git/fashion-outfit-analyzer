from django.db import models

class Product(models.Model):

    CATEGORY_CHOICES = [
        ("Shoes", "Shoes"),
        ("Bag", "Bag"),
        ("Watch", "Watch"),
        ("Belt", "Belt"),
        ("Jewellery", "Jewellery"),
        ("Accessory", "Accessory"),
    ]

    STYLE_CHOICES = [
        ("Casual", "Casual"),
        ("Formal", "Formal"),
        ("Streetwear", "Streetwear"),
        ("Traditional", "Traditional"),
        ("Sport", "Sport"),
        ("Minimal", "Minimal"),
    ]

    OCCASION_CHOICES = [
        ("College", "College"),
        ("Office", "Office"),
        ("Party", "Party"),
        ("Wedding", "Wedding"),
        ("Casual", "Casual"),
    ]

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    color = models.CharField(max_length=50)

    style = models.CharField(max_length=30, choices=STYLE_CHOICES)

    occasion = models.CharField(max_length=30, choices=OCCASION_CHOICES)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)

    image = models.ImageField(upload_to="products/")

    buy_link = models.URLField()

    store = models.CharField(max_length=50)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name