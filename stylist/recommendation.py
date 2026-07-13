import itertools

from .filters import get_items

from .selectors import (
    choose_best_bag,
    choose_best_accessory,
    choose_best_shoes
)

from .scoring import score_outfit

from .explanation import build_reason

from .diversity import remove_duplicate_outfits



def choose_best_outfits(items, occasion, weather):

    items = list(items)


    tops = get_items(
        items,
        "Top",
        occasion
    )


    bottoms = get_items(
        items,
        "Bottom",
        occasion
    )


    dresses = get_items(
        items,
        "Dress",
        occasion
    )


    shoes = get_items(
        items,
        "Shoes",
        occasion
    )


    bags = get_items(
        items,
        "Bag",
        occasion
    )


    accessories = get_items(
        items,
        "Accessory",
        occasion
    )



    outfits = []



    # =============================
    # DRESS OUTFITS
    # =============================

    for dress in dresses:


        shoe = choose_best_shoes(
            shoes,
            dress=dress,
            occasion=occasion
        )


        bag = choose_best_bag(
            bags,
            shoe,
            occasion
        )


        accessory = choose_best_accessory(
            accessories,
            bag,
            occasion
        )



        score, breakdown = score_outfit(

            dress=dress,

            shoes=shoe,

            bag=bag,

            accessory=accessory,

            occasion=occasion,

            weather=weather

        )



        outfits.append({

            "Dress": dress,

            "Shoes": shoe,

            "Bag": bag,

            "Accessory": accessory,

            "score": score,

            "breakdown": breakdown

        })





    # =============================
    # TOP + BOTTOM OUTFITS
    # =============================


    combinations = itertools.product(
        tops,
        bottoms
    )



    for top, bottom in combinations:


        shoe = choose_best_shoes(

            shoes,

            top=top,

            bottom=bottom,

            occasion=occasion

        )


        bag = choose_best_bag(

            bags,

            shoe,

            occasion

        )


        accessory = choose_best_accessory(

            accessories,

            bag,

            occasion

        )



        score, breakdown = score_outfit(

            top=top,

            bottom=bottom,

            shoes=shoe,

            bag=bag,

            accessory=accessory,

            occasion=occasion,

            weather=weather

        )



        outfits.append({

            "Top": top,

            "Bottom": bottom,

            "Shoes": shoe,

            "Bag": bag,

            "Accessory": accessory,

            "score": score,

            "breakdown": breakdown

        })





    # =============================
    # SORT BEST MATCH FIRST
    # =============================


    outfits.sort(

        key=lambda x: x["score"],

        reverse=True

    )





    # =============================
    # REMOVE DUPLICATE OUTFITS
    # KEEP TOP 3
    # =============================


    outfits = remove_duplicate_outfits(

        outfits,

        limit=3

    )





    # =============================
    # ADD AI EXPLANATION
    # =============================


    for outfit in outfits:


        outfit["reason"] = build_reason(

            outfit

        )




        # =============================
        # SHOPPING SEARCH QUERY
        # =============================


        search_items = []


        for key, item in outfit.items():


            if key in [
                "score",
                "breakdown",
                "reason"
            ]:

                continue



            if item:

                search_items.append(

                    item.name

                )



        outfit["search_query"] = " ".join(

            search_items

        )




    return outfits