WEATHER_SEASON = {
    "Sunny": "Summer",
    "Rainy": "Rainy",
    "Cold": "Winter",
    "Cloudy": "All Season",
}


TOP_CATEGORIES = {
    "Top",
    "Shirt",
    "T-shirt",
    "Hoodie",
    "Jacket",
}


OCCASION_COMPATIBILITY = {
    "Casual": {"Casual", "College"},
    "College": {"College", "Casual"},
    "Office": {"Office"},
    "Party": {"Party"},
    "Wedding": {"Wedding", "Party"},
}


STYLE_COMPATIBILITY = {
    "Casual": {"Casual", "Minimalist"},
    "Formal": {"Formal", "Elegant", "Minimalist"},
    "Business Casual": {
        "Business Casual",
        "Formal",
        "Minimalist",
        "Elegant",
    },
    "Party": {
        "Party",
        "Elegant",
        "Bohemian",
        "Vintage",
    },
    "Streetwear": {
        "Streetwear",
        "Sporty",
        "Casual",
    },
    "Sporty": {
        "Sporty",
        "Streetwear",
        "Casual",
    },
    "Traditional": {
        "Traditional",
        "Ethnic",
        "Elegant",
    },
    "Ethnic": {
        "Ethnic",
        "Traditional",
        "Elegant",
    },
    "Minimalist": {
        "Minimalist",
        "Casual",
        "Formal",
        "Business Casual",
    },
    "Vintage": {
        "Vintage",
        "Bohemian",
        "Elegant",
    },
    "Elegant": {
        "Elegant",
        "Formal",
        "Party",
        "Traditional",
        "Ethnic",
    },
    "Bohemian": {
        "Bohemian",
        "Vintage",
        "Party",
        "Casual",
    },
}


def filter_category(items, category):
    if category == "Top":
        return [
            item
            for item in items
            if item.category in TOP_CATEGORIES
        ]

    return [
        item
        for item in items
        if item.category == category
    ]


def is_occasion_compatible(item, occasion):
    if item is None or not occasion:
        return True

    allowed = OCCASION_COMPATIBILITY.get(occasion)

    if not allowed:
        return item.occasion == occasion

    return item.occasion in allowed


def filter_by_occasion(items, occasion):
    if not occasion:
        return list(items)

    return [
        item
        for item in items
        if is_occasion_compatible(
            item,
            occasion,
        )
    ]


def season_score(item, weather):
    if item is None or not weather:
        return 0

    if item.season == "All Season":
        return 10

    expected = WEATHER_SEASON.get(weather)

    if item.season == expected:
        return 20

    return 0


def is_season_compatible(item, weather):
    if item is None or not weather:
        return True

    if item.season == "All Season":
        return True

    expected = WEATHER_SEASON.get(weather)

    return item.season == expected


def is_style_compatible(item, preferred_style):
    if item is None or not preferred_style:
        return True

    allowed = STYLE_COMPATIBILITY.get(
        preferred_style
    )

    if not allowed:
        return item.style == preferred_style

    return item.style in allowed


def occasion_score(item, occasion):
    if item is None or not occasion:
        return 0

    if item.occasion == occasion:
        return 15

    allowed = OCCASION_COMPATIBILITY.get(
        occasion,
        set(),
    )

    if item.occasion in allowed:
        return 8

    return 0


def get_items(
    items,
    category,
    occasion,
    weather=None,
    style="",
):
    category_items = filter_category(
        items,
        category,
    )

    category_items = filter_by_occasion(
        category_items,
        occasion,
    )

    if weather:
        category_items = [
            item
            for item in category_items
            if is_season_compatible(
                item,
                weather,
            )
        ]

    if style:
        category_items = [
            item
            for item in category_items
            if is_style_compatible(
                item,
                style,
            )
        ]

    return category_items