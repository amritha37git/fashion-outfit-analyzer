def remove_duplicate_outfits(outfits, limit=3):
    """
    Return different outfit recommendations.
    Avoid repeating the same top, bottom or dress.
    """

    selected = []

    used_tops = set()
    used_bottoms = set()
    used_dresses = set()

    for outfit in outfits:

        top = outfit.get("Top")
        bottom = outfit.get("Bottom")
        dress = outfit.get("Dress")

        if top and top.id in used_tops:
            continue

        if bottom and bottom.id in used_bottoms:
            continue

        if dress and dress.id in used_dresses:
            continue

        if top:
            used_tops.add(top.id)

        if bottom:
            used_bottoms.add(bottom.id)

        if dress:
            used_dresses.add(dress.id)

        selected.append(outfit)

        if len(selected) >= limit:
            break

    return selected