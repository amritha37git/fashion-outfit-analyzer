from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from wardrobe.models import ClothingItem
from stylist.recommendation import choose_best_outfits

@login_required
def home(request):
    clothes = ClothingItem.objects.filter(user=request.user)
    recommendations = []

    # Generate AI outfit
    if clothes.exists():
        recommendations = choose_best_outfits(
            clothes,
            "Casual",
            "Sunny",
            "",
            ""
        )

    best_outfit = None
    ai_outfit_pieces = {}  # Create a clean dictionary for the template

    if recommendations:
        best_outfit = recommendations[0]
        # Safely extract your clothes dict so Django doesn't get confused
        ai_outfit_pieces = best_outfit.get('items', {})

    context = {
        "total_clothes": clothes.count(),
        "favourites": clothes.filter(favourite=True).count(),
        "recent_items": clothes.order_by("-created_at")[:6],
        "ai_outfit": best_outfit,
        "ai_outfit_pieces": ai_outfit_pieces,  # Pass it cleanly here
    }

    return render(request, "home.html", context)