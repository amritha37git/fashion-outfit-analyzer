from .color_match import color_score
from .filters import season_score, occasion_score


def style_score(item, preferred_style):
    """
    Returns style score out of 15
    """

    if item is None:
        return 0

    if not preferred_style:
        return 8

    if item.style == preferred_style:
        return 15

    return 0


def preference_score(item, preferred_color):
    """
    Returns color preference score out of 5
    """

    if item is None:
        return 0

    if not preferred_color:
        return 2

    if item.color.lower() == preferred_color.lower():
        return 5

    return 0


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
    FashionAI Outfit Score

    Total = 100

    Color Harmony      40
    Occasion           20
    Season             15
    Style              15
    User Preference     5
    Completeness        5
    """

    breakdown = {
        "color": 0,
        "occasion": 0,
        "season": 0,
        "style": 0,
        "preference": 0,
        "completeness": 0,
    }

    score = 0

    # -----------------------------
    # COLOR HARMONY (40)
    # -----------------------------

    if dress:

        if shoes:
            breakdown["color"] += color_score(
                dress.color,
                shoes.color
            )

        if bag:
            breakdown["color"] += color_score(
                dress.color,
                bag.color
            )

    else:

        if top and bottom:
            breakdown["color"] += color_score(
                top.color,
                bottom.color
            )

        if bottom and shoes:
            breakdown["color"] += color_score(
                bottom.color,
                shoes.color
            )

        if shoes and bag:
            breakdown["color"] += color_score(
                shoes.color,
                bag.color
            )

    breakdown["color"] = min(40, breakdown["color"])

    score += breakdown["color"]

    # -----------------------------
    # OCCASION (20)
    # -----------------------------

    occasion_points = 0

    for item in [
        top,
        bottom,
        dress,
        shoes,
        bag,
        accessory,
    ]:

        occasion_points += occasion_score(
            item,
            occasion
        )

    breakdown["occasion"] = min(20, occasion_points)

    score += breakdown["occasion"]

    # -----------------------------
    # WEATHER (15)
    # -----------------------------

    season_points = 0

    for item in [
        top,
        bottom,
        dress,
        shoes,
    ]:

        season_points += season_score(
            item,
            weather
        )

    breakdown["season"] = min(15, season_points)

    score += breakdown["season"]

    # -----------------------------
    # STYLE (15)
    # -----------------------------

    style_points = 0

    for item in [
        top,
        bottom,
        dress,
        shoes,
        bag,
        accessory,
    ]:

        style_points += style_score(
            item,
            style
        )

    breakdown["style"] = min(15, style_points)

    score += breakdown["style"]

    # -----------------------------
    # USER COLOR PREFERENCE (5)
    # -----------------------------

    preference_points = 0

    for item in [
        top,
        bottom,
        dress,
    ]:

        preference_points += preference_score(
            item,
            color
        )

    breakdown["preference"] = min(
        5,
        preference_points
    )

    score += breakdown["preference"]

    # -----------------------------
    # COMPLETENESS (5)
    # -----------------------------

    pieces = sum(
        x is not None
        for x in [
            top,
            bottom,
            dress,
            shoes,
            bag,
            accessory,
        ]
    )

    if pieces >= 5:
        breakdown["completeness"] = 5

    elif pieces == 4:
        breakdown["completeness"] = 4

    elif pieces == 3:
        breakdown["completeness"] = 3

    else:
        breakdown["completeness"] = 2

    score += breakdown["completeness"]

    score = min(score, 100)

    return score, breakdown