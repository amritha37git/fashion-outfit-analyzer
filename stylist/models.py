from django.db import models


class FashionProduct(models.Model):

    CATEGORY_CHOICES = [

        ("Shoes","Shoes"),
        ("Bag","Bag"),
        ("Accessory","Accessory"),
        ("Jewellery","Jewellery"),
        ("Watch","Watch"),
        ("Dress","Dress"),

    ]


    name = models.CharField(
        max_length=200
    )


    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )


    color = models.CharField(
        max_length=50
    )


    occasion = models.CharField(
        max_length=100
    )


    price = models.IntegerField()


    image = models.URLField(
        max_length=500
    )


    product_link = models.URLField(
        max_length=500
    )


    description = models.TextField(
        blank=True
    )


    def __str__(self):

        return self.name