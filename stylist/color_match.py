"""
ALAMARAi Color Matching Engine
"""


NEUTRAL_COLORS = [
    "White",
    "Black",
    "Grey",
    "Gray",
    "Beige",
    "Brown"
]


COLOR_MATCH = {

    "White": [
        "Black",
        "Blue",
        "Grey",
        "Gray",
        "Brown",
        "Beige",
        "Green",
        "Red"
    ],

    "Black": [
        "White",
        "Grey",
        "Gray",
        "Blue",
        "Brown",
        "Beige",
        "Red"
    ],

    "Blue": [
        "White",
        "Grey",
        "Gray",
        "Black",
        "Beige",
        "Brown"
    ],

    "Red": [
        "White",
        "Black",
        "Grey",
        "Gray"
    ],

    "Green": [
        "White",
        "Brown",
        "Beige"
    ],

    "Olive Green": [
        "White",
        "Black",
        "Brown",
        "Beige"
    ],

    "Yellow": [
        "White",
        "Blue",
        "Black"
    ],

    "Pink": [
        "White",
        "Grey",
        "Black"
    ],

    "Purple": [
        "White",
        "Grey",
        "Black"
    ],

    "Orange": [
        "White",
        "Black",
        "Brown"
    ],

    "Gold": [
        "Black",
        "White",
        "Brown"
    ]

}



def normalize(color):

    if not color:
        return ""

    return color.strip().title()



def colors_match(color1, color2):

    c1 = normalize(color1)

    c2 = normalize(color2)


    if not c1 or not c2:
        return False


    if c1 == c2:
        return True


    if c1 in NEUTRAL_COLORS:
        return True


    if c2 in NEUTRAL_COLORS:
        return True


    if c2 in COLOR_MATCH.get(c1, []):

        return True


    if c1 in COLOR_MATCH.get(c2, []):

        return True


    return False



def color_score(color1, color2):

    """
    Returns color compatibility score out of 15
    """

    c1 = normalize(color1)

    c2 = normalize(color2)


    if not c1 or not c2:
        return 0



    if c1 == c2:
        return 15



    if colors_match(c1,c2):

        if c1 in NEUTRAL_COLORS or c2 in NEUTRAL_COLORS:
            return 12

        return 10



    return 0