from django import forms
from .models import ClothingItem


class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem

        fields = [
            'name',
            'category',
            'brand',
            'color',
            'season',
            'occasion',
            'description',
            'image',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }