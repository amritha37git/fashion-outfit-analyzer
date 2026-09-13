import itertools

from .filters import get_items
from .selectors import (
    choose_best_bag,
    choose_best_accessory,
)
from .scoring import score_outfit
from .explanation import build_reason


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

MINIMUM_OUTFIT_SCORE = 60
MAX_RECOMMENDATIONS = 3


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

    Example:

    White top + blue jeans + white shoes

    repeated with another bag is NOT a new outfit.
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

    Different Top:
        +3

    Different Bottom:
        +3

    Different Dress:
        +3

    Different Shoes:
        +1
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

    This does NOT replace the main outfit score.

    It is only used to select the Trending Look from
    already-good candidates.
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

    # Style is the strongest trend signal.
    trend_score = (
        style_points * 2
        + color_points
        + supporting_points
    )

    return trend_score


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
    Add the strongest compatible bag and accessory.

    Accessories are optional.

    They improve a good outfit but do not replace the
    quality of the core outfit.
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

    Separates:
        Top × Bottom × Shoes

    Dresses:
        Dress × Shoes

    Bags and accessories are added after the core outfit
    is established.
    """

    candidates = []

    # -----------------------------------------------------
    # FILTER WARDROBE
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # DRESS + SHOES
    # -----------------------------------------------------

    for dress, shoe in itertools.product(
        dresses,
        shoes,
    ):

        outfit = {
            "Top": None,
            "Bottom": None,
            "Dress": dress,
            "Shoes": shoe,
            "Bag": None,
            "Accessory": None,
        }

        # First evaluate the core outfit.
        score, breakdown = score_outfit(
            dress=dress,
            shoes=shoe,
            occasion=occasion,
            weather=weather,
            style=style,
            color=color,
        )

        # Invalid core outfit.
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

        # Recalculate with supporting items.
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
        shoes,
    ):

        # -------------------------------------------------
        # IMPORTANT:
        #
        # Evaluate the actual Top + Bottom + Shoes
        # combination first.
        # -------------------------------------------------

        score, breakdown = score_outfit(
            top=top,
            bottom=bottom,
            shoes=shoe,
            occasion=occasion,
            weather=weather,
            style=style,
            color=color,
        )

        # Reject combinations that are fundamentally bad.
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

        # Re-score the complete outfit.
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
    Best Match is simply the strongest complete outfit.
    """

    if not candidates:
        return None

    return max(
        candidates,
        key=calculate_candidate_score,
    )


# ---------------------------------------------------------
# SELECT ALTERNATIVE
# ---------------------------------------------------------

def select_alternative(
    candidates,
    selected
):
    """
    Alternative Look:

    - Must be good enough.
    - Must have a different core clothing combination.
    - Should remain close to the best score.
    - Prefers meaningful clothing variation.
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

        # Do not choose something dramatically worse.
        if score < best_score - 15:
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

    if not alternative_candidates:
        return None

    alternative_candidates.sort(
        key=lambda value: value[0],
        reverse=True,
    )

    return alternative_candidates[0][1]


# ---------------------------------------------------------
# SELECT TRENDING
# ---------------------------------------------------------

def select_trending(
    candidates,
    selected
):
    """
    Trending Look:

    - Must still be a genuinely good outfit.
    - Must be different from the already selected looks.
    - Gives extra weight to style and color character.
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

        # Main outfit score remains dominant.
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

    if not trending_candidates:
        return None

    trending_candidates.sort(
        key=lambda value: value[0],
        reverse=True,
    )

    return trending_candidates[0][1]


# ---------------------------------------------------------
# FINAL SELECTION
# ---------------------------------------------------------

def select_best_outfits(candidates):
    """
    Create the three ALAMARAi recommendation roles:

        1. Best Match
        2. Alternative Look
        3. Trending Look

    No wardrobe-item reuse restriction exists.

    Only duplicate core combinations are prevented.
    """

    valid_candidates = [
        candidate
        for candidate in candidates
        if calculate_candidate_score(candidate)
        >= MINIMUM_OUTFIT_SCORE
    ]

    if not valid_candidates:
        return []

    # -----------------------------------------------------
    # BEST MATCH
    # -----------------------------------------------------

    best_match = select_best_match(
        valid_candidates
    )

    if not best_match:
        return []

    selected = [
        best_match
    ]

    # -----------------------------------------------------
    # ALTERNATIVE
    # -----------------------------------------------------

    alternative = select_alternative(
        valid_candidates,
        best_match,
    )

    if alternative:
        selected.append(
            alternative
        )

    # -----------------------------------------------------
    # TRENDING
    # -----------------------------------------------------

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

    Process:

    1. Load the user's wardrobe.
    2. Filter suitable wardrobe items.
    3. Generate all possible core combinations.
    4. Validate the core outfit.
    5. Find matching shoes/accessories.
    6. Score the complete outfit.
    7. Remove weak combinations.
    8. Select Best Match.
    9. Select Alternative Look.
    10. Select Trending Look.
    """

    items = list(items)

    if not items:
        return []

    # -----------------------------------------------------
    # GENERATE ALL CANDIDATES
    # -----------------------------------------------------

    candidates = build_candidates(
        items,
        occasion,
        weather,
        style,
        color,
    )

    # -----------------------------------------------------
    # SELECT FINAL RECOMMENDATIONS
    # -----------------------------------------------------

    final_outfits = select_best_outfits(
        candidates
    )

    # -----------------------------------------------------
    # ADD EXPLANATIONS
    # -----------------------------------------------------

    for outfit in final_outfits:

        outfit["reason"] = build_reason(
            outfit
        )

        # -------------------------------------------------
        # SEARCH QUERY
        # -------------------------------------------------

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

        # -------------------------------------------------
        # SHOPPING QUERY
        # -------------------------------------------------

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