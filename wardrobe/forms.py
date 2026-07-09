from django import forms
from .models import ClothingItem


class ClothingItemForm(forms.ModelForm):

    class Meta:

        model = ClothingItem

        fields = [
            "name",
            "category",
            "brand",
            "color",
            "season",
            "occasion",
            "description",
            "image",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Red Crop Top"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "brand": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Nike (Optional)"
                }
            ),

            "color": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Red"
                }
            ),

            "season": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "occasion": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your clothing item..."
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }

        labels = {

            "name": "Clothing Name",

            "category": "Category",

            "brand": "Brand",

            "color": "Color",

            "season": "Best Season",

            "occasion": "Suitable Occasion",

            "description": "Description",

            "image": "Upload Image",
        }

        help_texts = {

            "brand": "Leave as Unknown if not visible.",

            "image": "Upload a clear photo of a single clothing item."
        }

    def clean_name(self):

        name = self.cleaned_data["name"].strip()

        if len(name) < 2:

            raise forms.ValidationError(
                "Please enter a valid clothing name."
            )

        return name.title()

    def clean_brand(self):

        brand = self.cleaned_data.get("brand")

        if not brand:

            return "Unknown"

        return brand.title()

    def clean_color(self):

        color = self.cleaned_data["color"].strip()

        return color.title()