from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests

from wardrobe.models import ClothingItem
from stylist.recommendation import choose_best_outfits

from django.db.models import Count
from datetime import datetime


# ==================================
# LANDING PAGE
# ==================================

def landing_page(request):
    return render(request, "index.html")


# ==================================
# DASHBOARD
# ==================================

# ==================================
# DASHBOARD
# ==================================

@login_required
def home(request):

    # -----------------------------------
    # Get User Wardrobe
    # -----------------------------------

    clothes = ClothingItem.objects.filter(
        user=request.user
    )

    total_items = clothes.count()


    # -----------------------------------
    # Greeting
    # -----------------------------------

    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"


    # -----------------------------------
    # Outfit Recommendation
    # -----------------------------------

    recommended_outfits = []

    if clothes.exists():

        recommended_outfits = choose_best_outfits(
            clothes,
            "Casual",
            "Sunny",
            "",
            ""
        )


    today_outfit = None
    today_outfit_items = {}


    if recommended_outfits:

        today_outfit = recommended_outfits[0]

        today_outfit_items = today_outfit.get(
            "items",
            {}
        )



    # -----------------------------------
    # Weather
    # -----------------------------------

    weather = {

        "city": settings.CITY,

        "temperature": "--",

        "condition": "Unavailable",

        "icon": "",

        "humidity": "--",

        "wind": "--",

    }


    try:

        response = requests.get(

            "https://api.openweathermap.org/data/2.5/weather",

            params={

                "q": settings.CITY,

                "appid": settings.OPENWEATHER_API_KEY,

                "units": "metric",

            },

            timeout=5,

        )


        if response.status_code == 200:


            data = response.json()


            weather = {

                "city": data["name"],

                "temperature": round(
                    data["main"]["temp"]
                ),

                "condition": data["weather"][0]["main"],

                "icon": data["weather"][0]["icon"],

                "humidity": data["main"]["humidity"],

                "wind": round(
                    data["wind"]["speed"] * 3.6
                ),

            }


    except Exception:

        pass




    # -----------------------------------
    # Category Counts
    # -----------------------------------

    top_categories = [

        "Top",

        "Shirt",

        "T-shirt",

        "Hoodie",

        "Jacket",

    ]


    count_tops = clothes.filter(
        category__in=top_categories
    ).count()


    count_bottoms = clothes.filter(
        category="Bottom"
    ).count()


    count_dresses = clothes.filter(
        category="Dress"
    ).count()


    count_shoes = clothes.filter(
        category="Shoes"
    ).count()


    count_bags = clothes.filter(
        category="Bag"
    ).count()


    count_accessories = clothes.filter(
        category="Accessory"
    ).count()




    # -----------------------------------
    # Distribution Percentage
    # -----------------------------------

    def percentage(value):

        if total_items == 0:
            return 0

        return round(
            (value / total_items) * 100
        )


    dist_tops = percentage(count_tops)

    dist_bottoms = percentage(count_bottoms)

    dist_shoes = percentage(count_shoes)

    dist_accessories = percentage(count_accessories)




    # -----------------------------------
    # Latest Category Images
    # -----------------------------------

    latest_top = clothes.filter(
        category__in=top_categories
    ).first()


    latest_bottom = clothes.filter(
        category="Bottom"
    ).first()


    latest_dress = clothes.filter(
        category="Dress"
    ).first()


    latest_shoes = clothes.filter(
        category="Shoes"
    ).first()


    latest_bag = clothes.filter(
        category="Bag"
    ).first()


    latest_accessory = clothes.filter(
        category="Accessory"
    ).first()




    # -----------------------------------
    # Recent Activity
    # -----------------------------------

    recent_activity = clothes.order_by(
        "-created_at"
    )[:6]




    # -----------------------------------
    # Wardrobe Insights
    # -----------------------------------

    insights = []


    if total_items == 0:

        insights.append(
            "Your wardrobe is empty. Add clothing items to unlock insights."
        )


    else:


        favourite_count = clothes.filter(
            favourite=True
        ).count()


        if favourite_count:

            insights.append(
                f"You have {favourite_count} favourite items."
            )


        most_color = clothes.values(
            "color"
        ).annotate(
            total=Count("color")
        ).order_by(
            "-total"
        ).first()


        if most_color:

            insights.append(
                f"Your most common color is {most_color['color']}."
            )


        insights.append(
            f"You have {count_tops} tops in your wardrobe."
        )


        insights.append(
            f"You have {count_shoes} shoes available."
        )


        summer = clothes.filter(
            season="Summer"
        ).count()


        if summer:

            insights.append(
                f"{summer} items are suitable for summer."
            )


        casual = clothes.filter(
            occasion="Casual"
        ).count()


        if casual:

            insights.append(
                f"{casual} outfits are marked as casual wear."
            )




    # -----------------------------------
    # Context
    # -----------------------------------

    context = {


        # Greeting

        "greeting": greeting,



        # Statistics

        "total_items": total_items,

        "total_clothes": total_items,

        "favourites": clothes.filter(
            favourite=True
        ).count(),

        "recommended_looks": len(
            recommended_outfits
        ),



        # Categories

        "count_tops": count_tops,

        "count_bottoms": count_bottoms,

        "count_dresses": count_dresses,

        "count_shoes": count_shoes,

        "count_bags": count_bags,

        "count_accessories": count_accessories,


        "total_categories": 6,



        # Distribution

        "dist_tops": dist_tops,

        "dist_bottoms": dist_bottoms,

        "dist_shoes": dist_shoes,

        "dist_accessories": dist_accessories,



        # Images

        "latest_top": latest_top,

        "latest_bottom": latest_bottom,

        "latest_dress": latest_dress,

        "latest_shoes": latest_shoes,

        "latest_bag": latest_bag,

        "latest_accessory": latest_accessory,



        # Weather

        "weather": weather,



        # Insights

        "insights": insights,



        # Activity

        "recent_activity": recent_activity,

        "recent_items": recent_activity,



        # Recommendation

        "today_outfit": today_outfit,

        "today_outfit_items": today_outfit_items,


    }


    return render(

        request,

        "home.html",

        context

    )

# ==================================
# PROFILE SETTINGS
# ==================================

@login_required
def profile_view(request):
    return render(request, "profile.html")


@login_required
def profile_update(request):

    if request.method == "POST":
        # TODO:
        # Save user profile changes
        return redirect("profile")

    return redirect("profile")