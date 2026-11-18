import itertools
import random

from .filters import get_items
from .selectors import (
    choose_best_bag,
    choose_best_accessory,
    is_style_clashing,
)
from .scoring import score_outfit
from .explanation import build_reason


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

MINIMUM_OUTFIT_SCORE = 45
MAX_RECOMMENDATIONS = 3
VARIETY_SCORE_MARGIN = 8


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def get_item_id(item):
    """
    Return the database ID of an item.
    """

    if item is None:
        return None

    return item.pk


def calculate_candidate_score(outfit):
    """
    Safely return the numerical score.
    """

    return outfit.get(
        "score",
        0
    )


def core_signature(outfit):
    """
    Identify the actual clothing combination.

    This is used only to prevent the same core outfit
    from being displayed twice.

    Items themselves may be reused in other combinations.
    """

    return (
        get_item_id(
            outfit.get("Top")
        ),
        get_item_id(
            outfit.get("Bottom")
        ),
        get_item_id(
            outfit.get("Dress")
        ),
        get_item_id(
            outfit.get("Shoes")
        ),
    )


def is_same_core_outfit(
    outfit,
    selected_outfits
):
    """
    Reject only an identical core outfit.
    """

    current_signature = core_signature(
        outfit
    )

    for selected in selected_outfits:

        if (
            core_signature(selected)
            == current_signature
        ):
            return True

    return False


def core_difference_score(
    candidate,
    selected_outfits
):
    """
    Measure how different a candidate is from
    already selected recommendations.
    """

    if not selected_outfits:
        return 0

    score = 0

    for selected in selected_outfits:

        if (
            candidate.get("Top")
            and candidate.get("Top")
            != selected.get("Top")
        ):
            score += 3

        if (
            candidate.get("Bottom")
            and candidate.get("Bottom")
            != selected.get("Bottom")
        ):
            score += 3

        if (
            candidate.get("Dress")
            and candidate.get("Dress")
            != selected.get("Dress")
        ):
            score += 3

        if (
            candidate.get("Shoes")
            and candidate.get("Shoes")
            != selected.get("Shoes")
        ):
            score += 1

    return score


def get_trend_score(outfit):
    """
    Estimate the fashion/style strength of an outfit.
    """

    breakdown = outfit.get(
        "breakdown",
        {}
    )

    style_points = breakdown.get(
        "style",
        0
    )

    color_points = breakdown.get(
        "color",
        0
    )

    supporting_points = breakdown.get(
        "supporting_color",
        0
    )

    trend_score = (
        style_points * 2
        + color_points
        + supporting_points
    )

    return trend_score


def pick_weighted_top(scored_pairs, margin=VARIETY_SCORE_MARGIN):
    """
    Select an outfit from the top-scoring pool so repeated
    generations provide fresh recommendations while keeping
    scores high.
    """

    if not scored_pairs:
        return None

    scored_pairs.sort(key=lambda item: item[0], reverse=True)
    best_score = scored_pairs[0][0]

    top_pool = [
        (max(score, 1), candidate)
        for score, candidate in scored_pairs
        if score >= best_score - margin
    ]

    weights = [score for score, _ in top_pool]
    choices = [candidate for _, candidate in top_pool]

    return random.choices(choices, weights=weights, k=1)[0]


# ---------------------------------------------------------
# ACCESSORIES
# ---------------------------------------------------------

def add_best_accessories(
    outfit,
    bags,
    accessories,
    occasion,
    weather,
    style
):
    """
    Add a compatible bag and accessory.
    """

    shoes = outfit.get(
        "Shoes"
    )

    bag = choose_best_bag(
        bags,
        shoes,
        occasion,
        weather=weather,
        style=style,
    )

    accessory = choose_best_accessory(
        accessories,
        bag,
        occasion,
        weather=weather,
        style=style,
    )

    outfit["Bag"] = bag
    outfit["Accessory"] = accessory

    return outfit


# ---------------------------------------------------------
# BUILD CANDIDATES
# ---------------------------------------------------------

def build_candidates(
    items,
    occasion,
    weather,
    style,
    color
):
    """
    Generate all possible valid outfit combinations.
    """

    candidates = []

    tops = get_items(
        items,
        "Top",
        occasion,
        weather,
        style,
    )

    bottoms = get_items(
        items,
        "Bottom",
        occasion,
        weather,
        style,
    )

    dresses = get_items(
        items,
        "Dress",
        occasion,
        weather,
        style,
    )

    shoes = get_items(
        items,
        "Shoes",
        occasion,
        weather,
        style,
    )

    # Avoid pairing casual/sporty shoes with dressy occasions if non-clashing shoes exist
    non_clashing_shoes = [
        shoe for shoe in shoes
        if not is_style_clashing(shoe, occasion)
    ]
    if non_clashing_shoes:
        shoes = non_clashing_shoes

    bags = get_items(
        items,
        "Bag",
        occasion,
        weather,
        style,
    )

    accessories = get_items(
        items,
        "Accessory",
        occasion,
        weather,
        style,
    )

    shoe_options = shoes if shoes else [None]

    # -----------------------------------------------------
    # DRESS + SHOES
    # -----------------------------------------------------

    for dress, shoe in itertools.product(
        dresses,
        shoe_options,
    ):

        outfit = {
            "Top": None,
            "Bottom": None,
            "Dress": dress,
            "Shoes": shoe,
            "Bag": None,
            "Accessory": None,
        }

        score, breakdown = score_outfit(
            dress=dress,
            shoes=shoe,
            occasion=occasion,
            weather=weather,
            style=style,
            color=color,
        )

        if score <= 0:
            continue

        outfit = add_best_accessories(
            outfit,
            bags,
            accessories,
            occasion,
            weather,
            style,
        )

        score, breakdown = score_outfit(
            dress=dress,
            shoes=shoe,
            bag=outfit.get("Bag"),
            accessory=outfit.get("Accessory"),
            occasion=occasion,
            weather=weather,
            style=style,
            color=color,
        )

        outfit["score"] = score
        outfit["breakdown"] = breakdown

        candidates.append(
            outfit
        )

    # -----------------------------------------------------
    # TOP + BOTTOM + SHOES
    # -----------------------------------------------------

    for top, bottom, shoe in itertools.product(
        tops,
        bottoms,
        shoe_options,
    ):

        score, breakdown = score_outfit(
            top=top,
            bottom=bottom,
            shoes=shoe,
            occasion=occasion,
            weather=weather,
            style=style,
            color=color,
        )

        if score <= 0:
            continue

        outfit = {
            "Top": top,
            "Bottom": bottom,
            "Dress": None,
            "Shoes": shoe,
            "Bag": None,
            "Accessory": None,
        }

        outfit = add_best_accessories(
            outfit,
            bags,
            accessories,
            occasion,
            weather,
            style,
        )

        score, breakdown = score_outfit(
            top=top,
            bottom=bottom,
            shoes=shoe,
            bag=outfit.get("Bag"),
            accessory=outfit.get("Accessory"),
            occasion=occasion,
            weather=weather,
            style=style,
            color=color,
        )

        outfit["score"] = score
        outfit["breakdown"] = breakdown

        candidates.append(
            outfit
        )

    return candidates


# ---------------------------------------------------------
# SELECT BEST MATCH
# ---------------------------------------------------------

def select_best_match(candidates):
    """
    Select a top-scoring complete outfit with slight variety
    across runs.
    """

    if not candidates:
        return None

    scored_pairs = [
        (calculate_candidate_score(candidate), candidate)
        for candidate in candidates
    ]

    return pick_weighted_top(scored_pairs)


# ---------------------------------------------------------
# SELECT ALTERNATIVE
# ---------------------------------------------------------

def select_alternative(
    candidates,
    selected
):
    """
    Alternative Look:
    Different core clothing combination with variety across runs.
    """

    if not candidates:
        return None

    best_score = calculate_candidate_score(
        selected
    )

    alternative_candidates = []

    for candidate in candidates:

        if is_same_core_outfit(
            candidate,
            [selected]
        ):
            continue

        score = calculate_candidate_score(
            candidate
        )

        if score < best_score - 18:
            continue

        difference = core_difference_score(
            candidate,
            [selected]
        )

        alternative_candidates.append(
            (
                score + difference * 2,
                candidate,
            )
        )

    return pick_weighted_top(alternative_candidates)


# ---------------------------------------------------------
# SELECT TRENDING
# ---------------------------------------------------------

def select_trending(
    candidates,
    selected
):
    """
    Trending Look:
    Distinct look emphasizing style and color character.
    """

    if not candidates:
        return None

    trending_candidates = []

    for candidate in candidates:

        if is_same_core_outfit(
            candidate,
            selected
        ):
            continue

        difference = core_difference_score(
            candidate,
            selected
        )

        if difference <= 0:
            continue

        base_score = calculate_candidate_score(
            candidate
        )

        trend_score = get_trend_score(
            candidate
        )

        final_trend_score = (
            base_score * 2
            + trend_score
            + difference * 3
        )

        trending_candidates.append(
            (
                final_trend_score,
                candidate,
            )
        )

    return pick_weighted_top(trending_candidates)


# ---------------------------------------------------------
# FINAL SELECTION
# ---------------------------------------------------------

def select_best_outfits(candidates):
    """
    Create the three ALAMARAi recommendation roles:

    1. Best Match
    2. Alternative Look
    3. Trending Look
    """

    valid_candidates = [
        candidate
        for candidate in candidates
        if calculate_candidate_score(candidate)
        >= MINIMUM_OUTFIT_SCORE
    ]

    if not valid_candidates:
        return []

    best_match = select_best_match(
        valid_candidates
    )

    if not best_match:
        return []

    selected = [
        best_match
    ]

    alternative = select_alternative(
        valid_candidates,
        best_match,
    )

    if alternative:
        selected.append(
            alternative
        )

    trending = select_trending(
        valid_candidates,
        selected,
    )

    if trending:
        selected.append(
            trending
        )

    return selected[:MAX_RECOMMENDATIONS]


# ---------------------------------------------------------
# MAIN RECOMMENDATION FUNCTION
# ---------------------------------------------------------

def choose_best_outfits(
    items,
    occasion,
    weather,
    style="",
    color=""
):
    """
    Main ALAMARAi recommendation engine.
    """

    items = list(items)

    if not items:
        return []

    candidates = build_candidates(
        items,
        occasion,
        weather,
        style,
        color,
    )

    final_outfits = select_best_outfits(
        candidates
    )

    for outfit in final_outfits:

        outfit["reason"] = build_reason(
            outfit
        )

        search_parts = []

        for key, item in outfit.items():

            if key in {
                "score",
                "breakdown",
                "reason",
                "search_query",
                "shopping_query",
            }:
                continue

            if item is None:
                continue

            if hasattr(
                item,
                "name"
            ):
                search_parts.append(
                    item.name
                )

        outfit["search_query"] = (
            " ".join(
                search_parts
            )
        )

        keywords = []

        if style:
            keywords.append(
                style
            )

        if color:
            keywords.append(
                color
            )

        if occasion:
            keywords.append(
                occasion
            )

        if outfit.get(
            "Shoes"
        ):
            keywords.append(
                "Shoes"
            )

        if outfit.get(
            "Bag"
        ):
            keywords.append(
                "Bag"
            )

        if outfit.get(
            "Accessory"
        ):
            keywords.append(
                "Accessories"
            )

        outfit["shopping_query"] = (
            " ".join(
                keywords
            )
        )

    return final_outfits