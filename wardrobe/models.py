from django.db import models
from django.contrib.auth.models import User


class ClothingItem(models.Model):

    CATEGORY_CHOICES = [
        ("Top", "Top"),
        ("Bottom", "Bottom"),
        ("Dress", "Dress"),
        ("Shirt", "Shirt"),
        ("T-shirt", "T-shirt"),
        ("Hoodie", "Hoodie"),
        ("Jacket", "Jacket"),
        ("Shoes", "Shoes"),
        ("Bag", "Bag"),
        ("Accessory", "Accessory"),
    ]

    SEASON_CHOICES = [
        ("Summer", "Summer"),
        ("Winter", "Winter"),
        ("Rainy", "Rainy"),
        ("All Season", "All Season"),
    ]

    OCCASION_CHOICES = [
        ("Casual", "Casual"),
        ("College", "College"),
        ("Office", "Office"),
        ("Party", "Party"),
        ("Wedding", "Wedding"),
    ]

    STYLE_CHOICES = [
        ("Casual", "Casual"),
        ("Formal", "Formal"),
        ("Business Casual", "Business Casual"),
        ("Party", "Party"),
        ("Streetwear", "Streetwear"),
        ("Sporty", "Sporty"),
        ("Traditional", "Traditional"),
        ("Ethnic", "Ethnic"),
        ("Minimalist", "Minimalist"),
        ("Vintage", "Vintage"),
        ("Elegant", "Elegant"),
        ("Bohemian", "Bohemian"),
    ]

    # User relationship
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="clothes"
    )

    # Basic Information
    name = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    brand = models.CharField(
        max_length=100,
        default="Unknown",
        blank=True
    )

    color = models.CharField(
        max_length=50
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    image = models.ImageField(
        upload_to="wardrobe/"
    )

    # Fashion Information
    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES,
        default="All Season"
    )

    occasion = models.CharField(
        max_length=20,
        choices=OCCASION_CHOICES,
        default="Casual"
    )

    style = models.CharField(
        max_length=30,
        choices=STYLE_CHOICES,
        default="Casual"
    )

    # System Information
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.category})"