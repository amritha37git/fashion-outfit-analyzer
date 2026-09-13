from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from wardrobe.models import ClothingItem

from .recommendation import choose_best_outfits


@login_required
def stylist(request):

    recommendations = []

    occasion = ""
    weather = ""
    style = ""
    color = ""

    error_title = ""
    error_message = ""

    result_message = ""
    result_type = ""

    if request.method == "POST":

        occasion = request.POST.get(
            "occasion",
            ""
        ).strip()

        weather = request.POST.get(
            "weather",
            ""
        ).strip()

        style = request.POST.get(
            "style",
            ""
        ).strip()

        color = request.POST.get(
            "color",
            ""
        ).strip()

        clothes = ClothingItem.objects.filter(
            user=request.user
        )

        # -------------------------------------------------
        # EMPTY WARDROBE
        # -------------------------------------------------

        if not clothes.exists():

            error_title = "Wardrobe Empty"

            error_message = (
                "Upload clothing items before generating "
                "outfit recommendations."
            )

        else:

            outfits = choose_best_outfits(
                clothes,
                occasion,
                weather,
                style,
                color,
            )

            # -------------------------------------------------
            # REMOVE ANY INVALID / ZERO-SCORE OUTFITS
            # -------------------------------------------------

            outfits = [
                outfit
                for outfit in outfits
                if outfit.get("score", 0) > 0
            ]

            # -------------------------------------------------
            # NO SUITABLE OUTFIT
            # -------------------------------------------------

            if not outfits:

                error_title = "No Suitable Outfit"

                error_message = (
                    "No suitable outfit could be created "
                    "from your current wardrobe for the "
                    "selected occasion, weather and style. "
                    "Try changing the filters or adding "
                    "more suitable clothing items."
                )

            # -------------------------------------------------
            # VALID RECOMMENDATIONS
            # -------------------------------------------------

            else:

                count = len(outfits)

                if count == 1:

                    result_message = (
                        "1 suitable outfit found."
                    )

                elif count == 2:

                    result_message = (
                        "2 suitable outfits found."
                    )

                else:

                    result_message = (
                        "3 suitable outfits found."
                    )

                result_type = "success"

                titles = [
                    "Best Match",
                    "Alternative Look",
                    "Trending Look",
                ]

                categories = [
                    "Top",
                    "Bottom",
                    "Dress",
                    "Shoes",
                    "Bag",
                    "Accessory",
                ]

                # -------------------------------------------------
                # BUILD RECOMMENDATION DATA
                # -------------------------------------------------

                for index, outfit in enumerate(
                    outfits
                ):

                    score = outfit.get(
                        "score",
                        0
                    )

                    # Extra safety check.
                    if score <= 0:
                        continue

                    items = {}

                    for category in categories:

                        item = outfit.get(
                            category
                        )

                        if not item:
                            continue

                        items[category] = {
                            "name": item.name,
                            "color": item.color,
                            "brand": getattr(
                                item,
                                "brand",
                                "Unknown",
                            ),
                            "season": item.season,
                            "occasion": item.occasion,
                            "image": (
                                item.image.url
                                if item.image
                                else ""
                            ),
                        }

                    recommendations.append({

                        "title": (
                            titles[index]
                            if index < len(titles)
                            else "Outfit"
                        ),

                        "score": score,

                        "reason": outfit.get(
                            "reason",
                            ""
                        ),

                        "breakdown": outfit.get(
                            "breakdown",
                            {}
                        ),

                        "items": items,

                    })

                # -------------------------------------------------
                # FINAL SAFETY CHECK
                # -------------------------------------------------

                if not recommendations:

                    error_title = (
                        "No Suitable Outfit"
                    )

                    error_message = (
                        "No suitable outfit could be "
                        "created from your current wardrobe. "
                        "Try changing the filters or adding "
                        "more suitable clothing items."
                    )

                    result_message = ""
                    result_type = ""

    return render(
        request,
        "stylist.html",
        {
            "recommendations": recommendations,

            "selected_occasion": occasion,

            "selected_weather": weather,

            "selected_style": style,

            "selected_color": color,

            "error_title": error_title,

            "error_message": error_message,

            "result_message": result_message,

            "result_type": result_type,
        }
    )