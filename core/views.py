from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from wardrobe.models import ClothingItem
from stylist.recommendation import choose_best_outfits



# ==================================
# LANDING PAGE
# ==================================

def landing_page(request):

    return render(
        request,
        "index.html"
    )





# ==================================
# DASHBOARD
# ==================================

@login_required
def home(request):


    clothes = ClothingItem.objects.filter(
        user=request.user
    )



    recommendations = []



    if clothes.exists():

        recommendations = choose_best_outfits(
            clothes,
            "Casual",
            "Sunny",
            "",
            ""
        )




    best_outfit = None

    ai_outfit_pieces = {}



    if recommendations:

        best_outfit = recommendations[0]

        ai_outfit_pieces = best_outfit.get(
            "items",
            {}
        )





    # ===============================
    # CATEGORY STATISTICS
    # ===============================


    category_counts = {


        "tops":
            clothes.filter(
                category__in=[
                    "Top",
                    "Shirt",
                    "T-shirt",
                    "Hoodie",
                    "Jacket"
                ]
            ).count(),



        "bottoms":
            clothes.filter(
                category="Bottom"
            ).count(),



        "dresses":
            clothes.filter(
                category="Dress"
            ).count(),



        "shoes":
            clothes.filter(
                category="Shoes"
            ).count(),



        "bags":
            clothes.filter(
                category="Bag"
            ).count(),



        "accessories":
            clothes.filter(
                category="Accessory"
            ).count(),

    }





    context = {


        # Main Stats

        "total_clothes":
            clothes.count(),



        "favourites":
            clothes.filter(
                favourite=True
            ).count(),




        "ai_matches":
            len(recommendations),




        "shopping_picks":
            0,





        # Category Stats

        "category_counts":
            category_counts,





        # Wardrobe

        "recent_items":
            clothes.order_by(
                "-created_at"
            )[:6],





        # Recommendation

        "ai_outfit":
            best_outfit,



        "ai_outfit_pieces":
            ai_outfit_pieces,



    }





    return render(
        request,
        "home.html",
        context
    )