from django.db import models
from django.contrib.auth.models import User


class ClothingItem(models.Model):

    CATEGORY_CHOICES = [
        ('Top', 'Top'),
        ('Bottom', 'Bottom'),
        ('Dress', 'Dress'),
        ('Shoes', 'Shoes'),
        ('Bag', 'Bag'),
        ('Accessory', 'Accessory'),
    ]

    SEASON_CHOICES = [
        ('Summer', 'Summer'),
        ('Winter', 'Winter'),
        ('Rainy', 'Rainy'),
        ('All Season', 'All Season'),
    ]

    OCCASION_CHOICES = [
        ('Casual', 'Casual'),
        ('College', 'College'),
        ('Office', 'Office'),
        ('Party', 'Party'),
        ('Wedding', 'Wedding'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    brand = models.CharField(
        max_length=100,
        blank=True
    )

    color = models.CharField(
        max_length=50
    )

    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES
    )

    occasion = models.CharField(
        max_length=20,
        choices=OCCASION_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to='wardrobe/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name