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


        occasion = request.POST.get(
            "occasion",
            ""
        )


        weather = request.POST.get(
            "weather",
            ""
        )



        clothes = ClothingItem.objects.filter(
            user=request.user
        )



        if not clothes.exists():


            error_title = "👗 Wardrobe Empty"


            error_message = (
                "Upload clothes to your wardrobe "
                "before generating recommendations."
            )



        else:


            outfits = choose_best_outfits(

                clothes,

                occasion,

                weather

            )



            if not outfits:


                error_title = "😔 No Outfit Found"


                error_message = (
                    "No suitable combination found. "
                    "Try adding more clothes."
                )



            else:


                titles = [

                    "🥇 Best Match",

                    "🌟 Alternative Style",

                    "🔥 Trendy Choice"

                ]



                for index, outfit in enumerate(outfits):


                    items = {}



                    categories = [

                        "Top",

                        "Bottom",

                        "Dress",

                        "Shoes",

                        "Bag",

                        "Accessory"

                    ]



                    for category in categories:


                        item = outfit.get(category)



                        if item:


                            items[category] = {


                                "name": item.name,


                                "color": item.color,


                                "brand":
                                    getattr(
                                        item,
                                        "brand",
                                        "Unknown"
                                    ),


                                "season": item.season,


                                "occasion": item.occasion,


                                "image":
                                    item.image.url
                                    if item.image
                                    else ""

                            }




                    recommendations.append({

                        "title":
                            titles[index]
                            if index < len(titles)
                            else "Outfit",


                        "score":
                            outfit.get(
                                "score",
                                0
                            ),


                        "reason":
                            outfit.get(
                                "reason",
                                ""
                            ),


                        "breakdown":
                            outfit.get(
                                "breakdown",
                                {}
                            ),


                        "items":
                            items

                    })



    return render(

        request,

        "stylist.html",

        {


            "recommendations":
                recommendations,


            "selected_occasion":
                occasion,


            "selected_weather":
                weather,


            "error_title":
                error_title,


            "error_message":
                error_message,

        }

    )