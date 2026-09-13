from .color_match import color_score
from .filters import (
    occasion_score,
    is_occasion_compatible,
    season_score,
    is_season_compatible,
    is_style_compatible,
)


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
    Choose the best bag for the outfit.

    Bag is OPTIONAL.

    Only compatible bags are considered.
    """

    if not bags:
        return None

    best = None
    best_score = -1

    for bag in bags:

        # -----------------------------------------------
        # OCCASION
        # -----------------------------------------------

        if occasion and not is_occasion_compatible(
            bag,
            occasion
        ):
            continue

        # -----------------------------------------------
        # WEATHER
        # -----------------------------------------------

        if weather and not is_season_compatible(
            bag,
            weather
        ):
            continue

        # -----------------------------------------------
        # STYLE
        # -----------------------------------------------

        if style and not is_style_compatible(
            bag,
            style
        ):
            continue

        score = 0

        # -----------------------------------------------
        # COLOR
        # -----------------------------------------------

        if shoes:

            score += safe_color_score(
                shoes.color,
                bag.color
            )

        # -----------------------------------------------
        # OCCASION SCORE
        # -----------------------------------------------

        score += occasion_score(
            bag,
            occasion
        )

        # -----------------------------------------------
        # WEATHER SCORE
        # -----------------------------------------------

        if weather:

            score += season_score(
                bag,
                weather
            )

        # -----------------------------------------------
        # EXACT STYLE BONUS
        # -----------------------------------------------

        if style:

            if bag.style == style:
                score += 10

        # -----------------------------------------------
        # BEST BAG
        # -----------------------------------------------

        if score > best_score:

            best_score = score
            best = bag

    return best


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
    Choose the best accessory.

    Examples:
        Earrings
        Necklace
        Bangles
        Bracelet
        Watch

    Accessory is OPTIONAL.
    """

    if not accessories:
        return None

    best = None
    best_score = -1

    for accessory in accessories:

        # -----------------------------------------------
        # OCCASION
        # -----------------------------------------------

        if occasion and not is_occasion_compatible(
            accessory,
            occasion
        ):
            continue

        # -----------------------------------------------
        # WEATHER
        # -----------------------------------------------

        if weather and not is_season_compatible(
            accessory,
            weather
        ):
            continue

        # -----------------------------------------------
        # STYLE
        # -----------------------------------------------

        if style and not is_style_compatible(
            accessory,
            style
        ):
            continue

        score = 0

        # -----------------------------------------------
        # OCCASION
        # -----------------------------------------------

        score += occasion_score(
            accessory,
            occasion
        )

        # -----------------------------------------------
        # WEATHER
        # -----------------------------------------------

        if weather:

            score += season_score(
                accessory,
                weather
            )

        # -----------------------------------------------
        # BAG COLOR
        # -----------------------------------------------

        if bag:

            score += safe_color_score(
                accessory.color,
                bag.color
            )

        # -----------------------------------------------
        # EXACT STYLE BONUS
        # -----------------------------------------------

        if style:

            if accessory.style == style:
                score += 10

        # -----------------------------------------------
        # BEST ACCESSORY
        # -----------------------------------------------

        if score > best_score:

            best_score = score
            best = accessory

    return best


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
    Select the best shoes for the outfit.

    Shoes are REQUIRED for a complete recommendation.
    """

    if not shoes:
        return None

    best = None
    best_score = -1

    for shoe in shoes:

        # -----------------------------------------------
        # OCCASION
        # -----------------------------------------------

        if occasion and not is_occasion_compatible(
            shoe,
            occasion
        ):
            continue

        # -----------------------------------------------
        # WEATHER
        # -----------------------------------------------

        if weather and not is_season_compatible(
            shoe,
            weather
        ):
            continue

        # -----------------------------------------------
        # STYLE
        # -----------------------------------------------

        if style and not is_style_compatible(
            shoe,
            style
        ):
            continue

        score = 0

        # -----------------------------------------------
        # OCCASION
        # -----------------------------------------------

        score += occasion_score(
            shoe,
            occasion
        )

        # -----------------------------------------------
        # WEATHER
        # -----------------------------------------------

        if weather:

            score += season_score(
                shoe,
                weather
            )

        # -----------------------------------------------
        # COLOR MATCH
        # -----------------------------------------------

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

        # -----------------------------------------------
        # EXACT STYLE BONUS
        # -----------------------------------------------

        if style:

            if shoe.style == style:
                score += 10

        # -----------------------------------------------
        # BEST SHOES
        # -----------------------------------------------

        if score > best_score:

            best_score = score
            best = shoe

    return best