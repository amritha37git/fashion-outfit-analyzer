from .color_match import color_score
from .filters import season_score, occasion_score


def score_outfit(
    top=None,
    bottom=None,
    dress=None,
    shoes=None,
    bag=None,
    accessory=None,
    occasion=None,
    weather=None,
):
    """
    Returns:
        total_score,
        breakdown
    """

    breakdown = {
        "color": 0,
        "occasion": 0,
        "season": 0,
        "style": 0,
    }

    score = 0

    # -----------------------
    # COLOR
    # -----------------------

    if dress:

        if shoes:
            value = color_score(dress.color, shoes.color)
            score += value
            breakdown["color"] += value

        if bag:
            value = color_score(dress.color, bag.color)
            score += value
            breakdown["color"] += value

    else:

        if top and bottom:
            value = color_score(top.color, bottom.color)
            score += value
            breakdown["color"] += value

        if bottom and shoes:
            value = color_score(bottom.color, shoes.color)
            score += value
            breakdown["color"] += value

        if shoes and bag:
            value = color_score(shoes.color, bag.color)
            score += value
            breakdown["color"] += value

    # -----------------------
    # OCCASION
    # -----------------------

    for item in [top, bottom, dress, shoes, bag, accessory]:

        value = occasion_score(item, occasion)

        score += value
        breakdown["occasion"] += value

    # -----------------------
    # WEATHER
    # -----------------------

    for item in [top, bottom, dress, shoes]:

        value = season_score(item, weather)

        score += value
        breakdown["season"] += value

    # -----------------------
    # STYLE BONUS
    # -----------------------

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

    style = min(10 + pieces, 20)

    score += style
    breakdown["style"] = style

    # -----------------------
    # LIMIT SCORE
    # -----------------------

    score = min(score, 100)

    breakdown["color"] = min(breakdown["color"], 40)
    breakdown["occasion"] = min(breakdown["occasion"], 30)
    breakdown["season"] = min(breakdown["season"], 20)
    breakdown["style"] = min(breakdown["style"], 20)

    return score, breakdown