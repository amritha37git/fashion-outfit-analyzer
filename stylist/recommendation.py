import itertools

from .color_match import colors_match
from .occasion_rules import valid_occasion, valid_weather


def filter_items(items, category, occasion, weather):

    return [
        item
        for item in items
        if item.category == category
        and valid_occasion(item, occasion)
        and valid_weather(item, weather)
    ]


def score_outfit(top=None, bottom=None, dress=None,
                 shoes=None, bag=None, accessory=None):

    score = 0

    breakdown = {
        "color": 0,
        "style": 0,
        "bag": 0,
        "accessory": 0
    }

    # ---------- COLOR ----------

    if dress:

        if shoes and colors_match(dress.color, shoes.color):
            score += 25
            breakdown["color"] += 25

        if bag and colors_match(dress.color, bag.color):
            score += 10
            breakdown["color"] += 10

    else:

        if top and bottom and colors_match(top.color, bottom.color):
            score += 25
            breakdown["color"] += 25

        if bottom and shoes and colors_match(bottom.color, shoes.color):
            score += 10
            breakdown["color"] += 10

        if top and bag and colors_match(top.color, bag.color):
            score += 5
            breakdown["color"] += 5

    # ---------- STYLE ----------

    score += 30
    breakdown["style"] = 30

    # ---------- BAG ----------

    if bag:
        score += 15
        breakdown["bag"] = 15

    # ---------- ACCESSORY ----------

    if accessory:
        score += 15
        breakdown["accessory"] = 15

    return score, breakdown


def build_reason(outfit):

    if outfit.get("Dress"):

        return (
            f"The {outfit['Dress'].color.lower()} dress is the centerpiece. "
            f"The selected shoes, bag and accessory complement the outfit, "
            f"creating a balanced and stylish look suitable for the chosen occasion."
        )

    return (
        f"The {outfit['Top'].color.lower()} {outfit['Top'].name} pairs well with the "
        f"{outfit['Bottom'].color.lower()} {outfit['Bottom'].name}. "
        f"The shoes and accessories complete the outfit while maintaining "
        f"good color harmony and style."
    )


def choose_best_outfits(items, occasion, weather):

    tops = filter_items(items, "Top", occasion, weather)
    bottoms = filter_items(items, "Bottom", occasion, weather)
    dresses = filter_items(items, "Dress", occasion, weather)
    shoes = filter_items(items, "Shoes", occasion, weather)
    bags = filter_items(items, "Bag", occasion, weather)
    accessories = filter_items(items, "Accessory", occasion, weather)

    outfits = []

    # ---------- Dress outfits ----------

    for dress in dresses:

        for shoe in shoes:

            bag = bags[0] if bags else None
            accessory = accessories[0] if accessories else None

            score, breakdown = score_outfit(
                dress=dress,
                shoes=shoe,
                bag=bag,
                accessory=accessory
            )

            outfits.append({

                "Dress": dress,
                "Shoes": shoe,
                "Bag": bag,
                "Accessory": accessory,

                "score": score,

                "breakdown": breakdown,

                "reason": build_reason({
                    "Dress": dress,
                    "Shoes": shoe,
                    "Bag": bag,
                    "Accessory": accessory
                })

            })

    # ---------- Top + Bottom outfits ----------

    for top, bottom, shoe in itertools.product(
            tops,
            bottoms,
            shoes):

        bag = bags[0] if bags else None
        accessory = accessories[0] if accessories else None

        score, breakdown = score_outfit(
            top=top,
            bottom=bottom,
            shoes=shoe,
            bag=bag,
            accessory=accessory
        )

        outfits.append({

            "Top": top,
            "Bottom": bottom,
            "Shoes": shoe,
            "Bag": bag,
            "Accessory": accessory,

            "score": score,

            "breakdown": breakdown,

            "reason": build_reason({
                "Top": top,
                "Bottom": bottom,
                "Shoes": shoe,
                "Bag": bag,
                "Accessory": accessory
            })

        })

    outfits.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return outfits[:3]