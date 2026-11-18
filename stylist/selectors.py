import random

from .color_match import color_score
from .filters import (
    occasion_score,
    is_occasion_compatible,
    season_score,
    is_season_compatible,
    is_style_compatible,
)


CASUAL_STYLES = {"Casual", "Sporty", "Streetwear"}
DRESSY_OCCASIONS = {"Party", "Wedding"}


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def safe_color_score(color1, color2):
    """
    Safely calculate color compatibility.
    """

    if not color1 or not color2:
        return 0

    return color_score(
        color1,
        color2
    )


def is_style_clashing(item, occasion):
    """
    Prevent casual/sporty bags or accessories from being
    forced onto dressy Party or Wedding outfits.
    """

    if item is None or not occasion:
        return False

    if occasion in DRESSY_OCCASIONS and item.style in CASUAL_STYLES:
        return True

    return False


# ---------------------------------------------------------
# BAG
# ---------------------------------------------------------

def choose_best_bag(
    bags,
    shoes,
    occasion,
    weather=None,
    style=""
):
    """
    Choose a compatible bag for the outfit.

    Bag is OPTIONAL. If no occasion-appropriate bag exists,
    returns None rather than forcing a clashing bag.
    """

    if not bags:
        return None

    scored_bags = []

    for bag in bags:

        if is_style_clashing(bag, occasion):
            continue

        if occasion and not is_occasion_compatible(
            bag,
            occasion,
            is_supporting=True,
        ):
            continue

        score = 0

        if shoes:
            score += safe_color_score(
                shoes.color,
                bag.color
            )

        score += occasion_score(
            bag,
            occasion
        )

        if weather and is_season_compatible(bag, weather):
            score += season_score(
                bag,
                weather
            )

        if style:
            if bag.style == style:
                score += 10
            elif is_style_compatible(bag, style):
                score += 5

        scored_bags.append((score, bag))

    if not scored_bags:
        return None

    scored_bags.sort(key=lambda x: x[0], reverse=True)
    top_score = scored_bags[0][0]

    # Pick randomly among top-scoring bags within 5 points for variety
    top_choices = [
        bag for score, bag in scored_bags
        if score >= top_score - 5
    ]

    return random.choice(top_choices)


# ---------------------------------------------------------
# ACCESSORY
# ---------------------------------------------------------

def choose_best_accessory(
    accessories,
    bag,
    occasion,
    weather=None,
    style=""
):
    """
    Choose a compatible accessory.

    Accessory is OPTIONAL.
    """

    if not accessories:
        return None

    scored_accessories = []

    for accessory in accessories:

        if is_style_clashing(accessory, occasion):
            continue

        if occasion and not is_occasion_compatible(
            accessory,
            occasion,
            is_supporting=True,
        ):
            continue

        score = 0

        score += occasion_score(
            accessory,
            occasion
        )

        if weather and is_season_compatible(accessory, weather):
            score += season_score(
                accessory,
                weather
            )

        if bag:
            score += safe_color_score(
                accessory.color,
                bag.color
            )

        if style:
            if accessory.style == style:
                score += 10
            elif is_style_compatible(accessory, style):
                score += 5

        scored_accessories.append((score, accessory))

    if not scored_accessories:
        return None

    scored_accessories.sort(key=lambda x: x[0], reverse=True)
    top_score = scored_accessories[0][0]

    top_choices = [
        acc for score, acc in scored_accessories
        if score >= top_score - 5
    ]

    return random.choice(top_choices)


# ---------------------------------------------------------
# SHOES
# ---------------------------------------------------------

def choose_best_shoes(
    shoes,
    top=None,
    bottom=None,
    dress=None,
    occasion=None,
    weather=None,
    style=""
):
    """
    Select compatible shoes for the outfit.
    """

    if not shoes:
        return None

    scored_shoes = []

    for shoe in shoes:

        if is_style_clashing(shoe, occasion):
            continue

        if occasion and not is_occasion_compatible(
            shoe,
            occasion,
            is_supporting=True,
        ):
            continue

        score = 0

        score += occasion_score(
            shoe,
            occasion
        )

        if weather and is_season_compatible(shoe, weather):
            score += season_score(
                shoe,
                weather
            )

        if dress:
            score += safe_color_score(
                dress.color,
                shoe.color
            )
        else:
            if bottom:
                score += safe_color_score(
                    bottom.color,
                    shoe.color
                )
            if top:
                score += safe_color_score(
                    top.color,
                    shoe.color
                )

        if style:
            if shoe.style == style:
                score += 10
            elif is_style_compatible(shoe, style):
                score += 5

        scored_shoes.append((score, shoe))

    if not scored_shoes:
        return shoes[0]

    scored_shoes.sort(key=lambda x: x[0], reverse=True)
    top_score = scored_shoes[0][0]

    top_choices = [
        shoe for score, shoe in scored_shoes
        if score >= top_score - 5
    ]

    return random.choice(top_choices)