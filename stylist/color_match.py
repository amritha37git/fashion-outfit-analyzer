NEUTRAL = {
    "White",
    "Black",
    "Grey",
    "Gray",
    "Beige",
    "Brown",
    "Cream"
}

COLOR_MATCH = {

    "White": ["Black","Blue","Grey","Brown","Green","Pink","Purple","Red"],

    "Black": ["White","Grey","Blue","Beige","Brown","Red"],

    "Blue": ["White","Grey","Beige","Brown"],

    "Red": ["White","Black","Grey"],

    "Green": ["White","Brown","Beige"],

    "Yellow": ["White","Blue","Black"],

    "Pink": ["White","Grey"],

    "Purple": ["White","Grey"],

    "Orange": ["White","Brown"],

    "Brown": ["White","Beige","Cream"],

    "Beige": ["White","Brown","Black"]
}


def colors_match(color1, color2):

    if not color1 or not color2:
        return False

    c1 = color1.title()
    c2 = color2.title()

    if c1 == c2:
        return True

    if c1 in NEUTRAL:
        return True

    if c2 in NEUTRAL:
        return True

    return c2 in COLOR_MATCH.get(c1, [])