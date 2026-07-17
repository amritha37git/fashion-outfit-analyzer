"""
Filtering helpers for ALAMARAi Stylist
"""

WEATHER_SEASON = {
    "Sunny": "Summer",
    "Rainy": "Rainy",
    "Cold": "Winter",
    "Cloudy": "All Season",
}


def filter_category(items, category):
    return [i for i in items if i.category == category]


def filter_by_occasion(items, occasion):
    """
    Priority:
    1. Exact occasion
    2. Casual
    3. All items
    """

    exact = [i for i in items if i.occasion == occasion]

    if exact:
        return exact

    casual = [i for i in items if i.occasion == "Casual"]

    if casual:
        return casual

    return list(items)


def season_score(item, weather):
    if item is None:
        return 0

    if item.season == "All Season":
        return 10

    expected = WEATHER_SEASON.get(weather)

    if item.season == expected:
        return 20

    return 0


def occasion_score(item, occasion):
    if item is None:
        return 0

    if item.occasion == occasion:
        return 15

    if item.occasion == "Casual":
        return 8

    return 0


def get_items(items, category, occasion):
    """
    Returns filtered items of one category.
    """

    category_items = filter_category(items, category)

    return filter_by_occasion(category_items, occasion)