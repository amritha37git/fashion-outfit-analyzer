from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "style",
        "occasion",
        "price",
        "store",
    )

    list_filter = (
        "category",
        "style",
        "occasion",
        "store",
    )

    search_fields = (
        "name",
        "brand",
        "color",
    )