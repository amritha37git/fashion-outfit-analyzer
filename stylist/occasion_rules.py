OCCASION_MAP = {

    "College": ["College", "Casual"],

    "Casual": ["Casual", "College"],

    "Office": ["Office"],

    "Party": ["Party", "Casual"],

    "Wedding": ["Wedding", "Party"]
}


WEATHER_MAP = {

    "Sunny": ["Summer", "All Season"],

    "Cloudy": ["All Season"],

    "Rainy": ["Rainy", "All Season"],

    "Cold": ["Winter", "All Season"]
}


def valid_occasion(item, occasion):

    allowed = OCCASION_MAP.get(occasion, [])

    return item.occasion in allowed


def valid_weather(item, weather):

    allowed = WEATHER_MAP.get(weather, [])

    return item.season in allowed