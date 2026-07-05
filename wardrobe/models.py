from django.db import models
from django.contrib.auth.models import User

class ClothingItem(models.Model):
    CATEGORY_CHOICES = [
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('dress', 'Dress'),
        ('shoes', 'Shoes'),
        ('accessory', 'Accessory'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='wardrobe/')
    color = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name