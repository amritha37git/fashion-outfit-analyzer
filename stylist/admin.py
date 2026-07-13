from django.contrib import admin

from .models import FashionProduct



@admin.register(FashionProduct)
class FashionProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'occasion',
        'price'
    )


    search_fields = (
        'name',
        'category',
        'occasion'
    )