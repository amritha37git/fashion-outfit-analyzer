from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from wardrobe.models import ClothingItem
from .recommendation import choose_best_outfits


@login_required
def stylist(request):

    recommendations = []
    occasion = ""
    weather = ""

    error_title = ""
    error_message = ""

    if request.method == "POST":

        occasion = request.POST.get("occasion")
        weather = request.POST.get("weather")

        clothes = ClothingItem.objects.filter(
            user=request.user
        )

        # Wardrobe is empty
        if not clothes.exists():

            error_title = "Your wardrobe is empty"

            error_message = (
                "Upload some clothing items before requesting outfit recommendations."
            )

        else:

            outfits = choose_best_outfits(
                clothes,
                occasion,
                weather
            )

            # No outfit found
            if not outfits:

                categories = set(
                    clothes.values_list("category", flat=True)
                )

                required = [
                    "Top",
                    "Bottom",
                    "Shoes",
                    "Bag",
                    "Accessory"
                ]

                missing = [
                    category
                    for category in required
                    if category not in categories
                ]

                if missing:

                    error_title = "Incomplete Wardrobe"

                    error_message = (
                        "You're missing: "
                        + ", ".join(missing)
                        + ". Upload these items for better recommendations."
                    )

                else:

                    error_title = "No Matching Outfit"

                    error_message = (
                        f"We couldn't create a complete {occasion} outfit "
                        f"for {weather.lower()} weather using your current wardrobe."
                    )

            else:

                titles = [
                    "🥇 Best Match",
                    "🌟 Alternative Look",
                    "🔥 Trendy Choice"
                ]

                for i, outfit in enumerate(outfits):

                    outfit_details = {}

                    for category in [
                        "Top",
                        "Bottom",
                        "Dress",
                        "Shoes",
                        "Bag",
                        "Accessory"
                    ]:

                        item = outfit.get(category)

                        if item:

                            outfit_details[category] = {
                                "name": item.name,
                                "color": item.color,
                                "brand": item.brand,
                                "season": item.season,
                                "occasion": item.occasion,
                                "image": item.image.url if item.image else ""
                            }

                    recommendations.append({

                        "title": titles[i] if i < len(titles) else f"Outfit {i+1}",

                        "score": outfit["score"],

                        "reason": outfit["reason"],

                        "breakdown": outfit["breakdown"],

                        "items": outfit_details

                    })

    return render(
        request,
        "stylist.html",
        {
            "recommendations": recommendations,
            "selected_occasion": occasion,
            "selected_weather": weather,
            "error_title": error_title,
            "error_message": error_message,
        }
    )