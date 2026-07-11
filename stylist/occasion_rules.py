def valid_occasion(item, selected_occasion):

    item_occasion = item.occasion


    # Exact match
    if item_occasion == selected_occasion:
        return True



    # Casual clothes are flexible

    if item_occasion == "Casual":

        if selected_occasion in [
            "College",
            "Casual"
        ]:
            return True



    # Party clothes can work for Wedding

    if item_occasion == "Party":

        if selected_occasion == "Wedding":
            return True



    # Wedding clothes can work for Party

    if item_occasion == "Wedding":

        if selected_occasion == "Party":
            return True



    return False





def valid_weather(item, weather):


    season = item.season



    weather_rules = {


        "Sunny": [

            "Summer",
            "All Season"

        ],



        "Cloudy": [

            "Summer",
            "Winter",
            "All Season"

        ],



        "Rainy": [

            "Rainy",
            "All Season"

        ],



        "Cold": [

            "Winter",
            "All Season"

        ]

    }



    allowed_seasons = weather_rules.get(
        weather,
        []
    )


    return season in allowed_seasons