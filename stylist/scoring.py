from .color_match import color_score
from .filters import (
    season_score,
    occasion_score,
    is_season_compatible,
    is_occasion_compatible,
    is_style_compatible,
)


# ---------------------------------------------------------
# STYLE SCORE
# ---------------------------------------------------------

def style_score(item, preferred_style):
    """
    Score how well an item fits the selected style.

    Exact style:
        15

    Compatible style:
        10

    No selected style:
        8

    Incompatible style:
        0
    """

    if item is None:
        return 0

    if not preferred_style:
        return 8

    if item.style == preferred_style:
        return 15

    if is_style_compatible(
        item,
        preferred_style
    ):
        return 10

    return 0


# ---------------------------------------------------------
# USER COLOR PREFERENCE
# ---------------------------------------------------------

def preference_score(item, preferred_color):
    """
    Score the user's selected color preference.
    """

    if item is None:
        return 0

    if not preferred_color:
        return 2

    item_color = (
        item.color or ""
    ).strip().lower()

    selected_color = (
        preferred_color or ""
    ).strip().lower()

    if not item_color:
        return 0

    if item_color == selected_color:
        return 5

    if (
        selected_color in item_color
        or item_color in selected_color
    ):
        return 3

    return 0


# ---------------------------------------------------------
# SAFE COLOR SCORE
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
# CORE COLOR HARMONY
# ---------------------------------------------------------

def calculate_core_color_score(
    top=None,
    bottom=None,
    dress=None,
    shoes=None,
):
    """
    Evaluate the main clothing combination.

    This is the most important color relationship.

    Top + Bottom is given the highest importance because
    they form the actual foundation of a separates outfit.

    Dress + Shoes is evaluated for dress outfits.
    """

    points = 0

    # -----------------------------------------------------
    # DRESS
    # -----------------------------------------------------

    if dress:

        if shoes:
            points += safe_color_score(
                dress.color,
                shoes.color
            )

        return min(
            30,
            points
        )

    # -----------------------------------------------------
    # TOP + BOTTOM
    # -----------------------------------------------------

    if top and bottom:

        points += safe_color_score(
            top.color,
            bottom.color
        )

    # -----------------------------------------------------
    # SHOES WITH CORE OUTFIT
    # -----------------------------------------------------

    if shoes:

        if bottom:
            points += int(
                safe_color_score(
                    bottom.color,
                    shoes.color
                ) * 0.5
            )

        elif top:
            points += int(
                safe_color_score(
                    top.color,
                    shoes.color
                ) * 0.5
            )

    return min(
        30,
        points
    )


# ---------------------------------------------------------
# SUPPORTING COLOR COORDINATION
# ---------------------------------------------------------

def calculate_supporting_color_score(
    top=None,
    bottom=None,
    dress=None,
    shoes=None,
    bag=None,
    accessory=None,
):
    """
    Evaluate bags and accessories after the core outfit
    has already been established.

    Supporting items can improve a look, but they cannot
    compensate for a poor core outfit.
    """

    points = 0

    reference_colors = []

    if dress:
        reference_colors.append(
            dress.color
        )

    if top:
        reference_colors.append(
            top.color
        )

    if bottom:
        reference_colors.append(
            bottom.color
        )

    if shoes:
        reference_colors.append(
            shoes.color
        )

    # -----------------------------------------------------
    # BAG
    # -----------------------------------------------------

    if bag and shoes:

        points += int(
            safe_color_score(
                shoes.color,
                bag.color
            ) * 0.6
        )

    elif bag and reference_colors:

        points += int(
            safe_color_score(
                reference_colors[0],
                bag.color
            ) * 0.4
        )

    # -----------------------------------------------------
    # ACCESSORY
    # -----------------------------------------------------

    if accessory:

        accessory_reference = (
            bag.color
            if bag
            else shoes.color
            if shoes
            else reference_colors[0]
            if reference_colors
            else None
        )

        if accessory_reference:

            points += int(
                safe_color_score(
                    accessory_reference,
                    accessory.color
                ) * 0.5
            )

    return min(
        10,
        points
    )


# ---------------------------------------------------------
# OCCASION SCORE
# ---------------------------------------------------------

def calculate_occasion_score(
    top,
    bottom,
    dress,
    shoes,
    bag,
    accessory,
    occasion
):
    """
    Evaluate how well the complete outfit suits
    the requested occasion.

    Core clothing receives more importance.
    """

    if not occasion:
        return 15

    points = 0

    core_items = [
        top,
        bottom,
        dress,
        shoes,
    ]

    supporting_items = [
        bag,
        accessory,
    ]

    # Core clothing
    for item in core_items:

        if item is None:
            continue

        if not is_occasion_compatible(
            item,
            occasion
        ):
            return 0

        points += occasion_score(
            item,
            occasion
        )

    # Supporting items
    for item in supporting_items:

        if item is None:
            continue

        if is_occasion_compatible(
            item,
            occasion
        ):
            points += int(
                occasion_score(
                    item,
                    occasion
                ) * 0.35
            )

    return min(
        20,
        points
    )


# ---------------------------------------------------------
# WEATHER SCORE
# ---------------------------------------------------------

def calculate_season_score(
    top,
    bottom,
    dress,
    shoes,
    bag,
    accessory,
    weather
):
    """
    Evaluate weather suitability.

    Core clothing has priority.
    """

    if not weather:
        return 12

    points = 0

    core_items = [
        top,
        bottom,
        dress,
        shoes,
    ]

    supporting_items = [
        bag,
        accessory,
    ]

    for item in core_items:

        if item is None:
            continue

        if not is_season_compatible(
            item,
            weather
        ):
            return 0

        points += season_score(
            item,
            weather
        )

    for item in supporting_items:

        if item is None:
            continue

        if is_season_compatible(
            item,
            weather
        ):
            points += int(
                season_score(
                    item,
                    weather
                ) * 0.25
            )

    return min(
        15,
        points
    )


# ---------------------------------------------------------
# STYLE SCORE
# ---------------------------------------------------------

def calculate_style_score(
    top,
    bottom,
    dress,
    shoes,
    bag,
    accessory,
    preferred_style
):
    """
    Evaluate consistency of the complete look.

    Main clothing pieces are more important than
    accessories.
    """

    if not preferred_style:
        return 12

    points = 0

    core_items = [
        top,
        bottom,
        dress,
        shoes,
    ]

    supporting_items = [
        bag,
        accessory,
    ]

    # Core style
    for item in core_items:

        if item is None:
            continue

        if not is_style_compatible(
            item,
            preferred_style
        ):
            return 0

        points += style_score(
            item,
            preferred_style
        )

    # Supporting style
    for item in supporting_items:

        if item is None:
            continue

        if is_style_compatible(
            item,
            preferred_style
        ):
            points += int(
                style_score(
                    item,
                    preferred_style
                ) * 0.25
            )

    return min(
        15,
        points
    )


# ---------------------------------------------------------
# USER PREFERENCE
# ---------------------------------------------------------

def calculate_preference_score(
    top,
    bottom,
    dress,
    preferred_color
):
    """
    Score the user's selected color preference.

    Main clothing pieces are considered.
    """

    if not preferred_color:
        return 2

    points = 0

    for item in [
        top,
        bottom,
        dress,
    ]:

        if item is not None:

            points += preference_score(
                item,
                preferred_color
            )

    return min(
        5,
        points
    )


# ---------------------------------------------------------
# COMPLETENESS
# ---------------------------------------------------------

def calculate_completeness(
    top,
    bottom,
    dress,
    shoes,
    bag,
    accessory
):
    """
    Evaluate whether the outfit contains the expected
    essential pieces.

    Bag and accessory are optional.
    """

    # Dress outfit
    if dress:

        if shoes:
            return 5

        return 2

    # Separates outfit
    if top and bottom:

        if shoes:
            return 5

        return 3

    return 1


# ---------------------------------------------------------
# MAIN OUTFIT SCORE
# ---------------------------------------------------------

def score_outfit(
    top=None,
    bottom=None,
    dress=None,
    shoes=None,
    bag=None,
    accessory=None,
    occasion=None,
    weather=None,
    style="",
    color="",
):
    """
    ALAMARAi Outfit Score

    Total = 100

    Core Color Harmony       30
    Supporting Coordination 10
    Occasion                 20
    Weather                  15
    Style                    15
    User Preference           5
    Completeness              5
    """

    breakdown = {
        "color": 0,
        "supporting_color": 0,
        "occasion": 0,
        "season": 0,
        "style": 0,
        "preference": 0,
        "completeness": 0,
    }

    # -----------------------------------------------------
    # BASIC VALIDITY
    # -----------------------------------------------------

    core_items = [
        item
        for item in [
            top,
            bottom,
            dress,
            shoes,
        ]
        if item is not None
    ]

    # Need a real core outfit.
    if dress:

        if shoes is None:
            return 0, breakdown

    elif top and bottom:

        if shoes is None:
            return 0, breakdown

    else:
        return 0, breakdown

    # -----------------------------------------------------
    # CORE OCCASION VALIDITY
    # -----------------------------------------------------

    if occasion:

        for item in core_items:

            if not is_occasion_compatible(
                item,
                occasion
            ):
                return 0, breakdown

    # -----------------------------------------------------
    # CORE WEATHER VALIDITY
    # -----------------------------------------------------

    if weather:

        for item in core_items:

            if not is_season_compatible(
                item,
                weather
            ):
                return 0, breakdown

    # -----------------------------------------------------
    # CORE STYLE VALIDITY
    # -----------------------------------------------------

    if style:

        for item in core_items:

            if not is_style_compatible(
                item,
                style
            ):
                return 0, breakdown

    # -----------------------------------------------------
    # CORE COLOR HARMONY
    # -----------------------------------------------------

    breakdown["color"] = calculate_core_color_score(
        top=top,
        bottom=bottom,
        dress=dress,
        shoes=shoes,
    )

    # -----------------------------------------------------
    # SUPPORTING COLOR COORDINATION
    # -----------------------------------------------------

    breakdown["supporting_color"] = (
        calculate_supporting_color_score(
            top=top,
            bottom=bottom,
            dress=dress,
            shoes=shoes,
            bag=bag,
            accessory=accessory,
        )
    )

    # -----------------------------------------------------
    # OCCASION
    # -----------------------------------------------------

    breakdown["occasion"] = (
        calculate_occasion_score(
            top,
            bottom,
            dress,
            shoes,
            bag,
            accessory,
            occasion,
        )
    )

    # -----------------------------------------------------
    # WEATHER
    # -----------------------------------------------------

    breakdown["season"] = (
        calculate_season_score(
            top,
            bottom,
            dress,
            shoes,
            bag,
            accessory,
            weather,
        )
    )

    # -----------------------------------------------------
    # STYLE
    # -----------------------------------------------------

    breakdown["style"] = (
        calculate_style_score(
            top,
            bottom,
            dress,
            shoes,
            bag,
            accessory,
            style,
        )
    )

    # -----------------------------------------------------
    # USER COLOR PREFERENCE
    # -----------------------------------------------------

    breakdown["preference"] = (
        calculate_preference_score(
            top,
            bottom,
            dress,
            color,
        )
    )

    # -----------------------------------------------------
    # COMPLETENESS
    # -----------------------------------------------------

    breakdown["completeness"] = (
        calculate_completeness(
            top,
            bottom,
            dress,
            shoes,
            bag,
            accessory,
        )
    )

    # -----------------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------------

    score = sum(
        breakdown.values()
    )

    return min(
        score,
        100
    ), breakdown