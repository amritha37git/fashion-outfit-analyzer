from .color_match import color_score


def choose_best_bag(bags, shoes, occasion):
    """
    Returns the best matching bag.
    """

    if not bags:
        return None

    best = None
    best_score = -1

    for bag in bags:

        score = 0

        if shoes:
            score += color_score(shoes.color, bag.color)

        if bag.occasion == occasion:
            score += 15
        elif bag.occasion == "Casual":
            score += 8

        if score > best_score:
            best_score = score
            best = bag

    return best


def choose_best_accessory(accessories, bag, occasion):
    """
    Returns the best accessory.
    """

    if not accessories:
        return None

    best = None
    best_score = -1

    for accessory in accessories:

        score = 0

        if accessory.occasion == occasion:
            score += 15
        elif accessory.occasion == "Casual":
            score += 8

        if bag:
            score += color_score(accessory.color, bag.color)

        if score > best_score:
            best_score = score
            best = accessory

    return best


def choose_best_shoes(shoes, top=None, bottom=None, dress=None, occasion=None):
    """
    Select the best shoes for the outfit.
    """

    if not shoes:
        return None

    best = None
    best_score = -1

    for shoe in shoes:

        score = 0

        if shoe.occasion == occasion:
            score += 15
        elif shoe.occasion == "Casual":
            score += 8

        if dress:
            score += color_score(dress.color, shoe.color)

        else:
            if bottom:
                score += color_score(bottom.color, shoe.color)

            elif top:
                score += color_score(top.color, shoe.color)

        if score > best_score:
            best_score = score
            best = shoe

    return best