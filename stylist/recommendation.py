import itertools

from .filters import get_items
from .selectors import (
    choose_best_bag,
    choose_best_accessory,
    choose_best_shoes,
)

from .scoring import score_outfit
from .explanation import build_reason
from .diversity import remove_duplicate_outfits


def choose_best_outfits(
    items,
    occasion,
    weather,
    style="",
    color=""
):

    items = list(items)

    tops = get_items(items, "Top", occasion)
    bottoms = get_items(items, "Bottom", occasion)
    dresses = get_items(items, "Dress", occasion)
    shoes = get_items(items, "Shoes", occasion)
    bags = get_items(items, "Bag", occasion)
    accessories = get_items(items, "Accessory", occasion)

    outfits = []

    # -----------------------------
    # Dress Based Outfits
    # -----------------------------

    for dress in dresses:

        shoe = choose_best_shoes(
            shoes,
            dress=dress,
            occasion=occasion,
        )

        bag = choose_best_bag(
            bags,
            shoe,
            occasion,
        )

        accessory = choose_best_accessory(
            accessories,
            bag,
            occasion,
        )

        score, breakdown = score_outfit(
            dress=dress,
            shoes=shoe,
            bag=bag,
            accessory=accessory,
            occasion=occasion,
            weather=weather,
            style=style,
            color=color,
        )

        outfits.append({
            "Dress": dress,
            "Shoes": shoe,
            "Bag": bag,
            "Accessory": accessory,
            "score": score,
            "breakdown": breakdown,
        })

    # -----------------------------
    # Top + Bottom Outfits
    # -----------------------------

    for top, bottom in itertools.product(tops, bottoms):

        shoe = choose_best_shoes(
            shoes,
            top=top,
            bottom=bottom,
            occasion=occasion,
        )

        bag = choose_best_bag(
            bags,
            shoe,
            occasion,
        )

        accessory = choose_best_accessory(
            accessories,
            bag,
            occasion,
        )

        score, breakdown = score_outfit(
            top=top,
            bottom=bottom,
            shoes=shoe,
            bag=bag,
            accessory=accessory,
            occasion=occasion,
            weather=weather,
            style=style,
            color=color,
        )

        outfits.append({
            "Top": top,
            "Bottom": bottom,
            "Shoes": shoe,
            "Bag": bag,
            "Accessory": accessory,
            "score": score,
            "breakdown": breakdown,
        })

    # Highest score first
    outfits.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    # Remove duplicate outfits
    outfits = remove_duplicate_outfits(
        outfits,
        limit=3,
    )

    # ----------------------------------
    # Generate explanation + shopping query
    # ----------------------------------

    for outfit in outfits:

        outfit["reason"] = build_reason(outfit)

        search_parts = []

        for key, item in outfit.items():

            if key in [
                "score",
                "breakdown",
                "reason",
            ]:
                continue

            if not item:
                continue

            search_parts.append(item.name)

        outfit["search_query"] = " ".join(search_parts)

        # -------- Better shopping suggestions --------

        keywords = []

        if style:
            keywords.append(style)

        if color:
            keywords.append(color)

        if occasion:
            keywords.append(occasion)

        if outfit.get("Shoes"):
            keywords.append("Shoes")

        if outfit.get("Bag"):
            keywords.append("Bag")

        if outfit.get("Accessory"):
            keywords.append("Watch")

        outfit["shopping_query"] = " ".join(keywords)

    return outfits