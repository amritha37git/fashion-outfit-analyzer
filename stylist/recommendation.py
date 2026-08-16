import itertools

from .filters import get_items
from .selectors import (
    choose_best_bag,
    choose_best_accessory,
    choose_best_shoes,
)

from .scoring import score_outfit
from .explanation import build_reason


def choose_best_outfits(
    items,
    occasion,
    weather,
    style="",
    color=""
):

    items = list(items)
    final_outfits = []

    # Loop exactly 3 times to get 3 completely unique outfits
    for _ in range(3):
        
        # Get the current pool of items (this shrinks every loop)
        tops = get_items(items, "Top", occasion)
        bottoms = get_items(items, "Bottom", occasion)
        dresses = get_items(items, "Dress", occasion)
        shoes = get_items(items, "Shoes", occasion)
        bags = get_items(items, "Bag", occasion)
        accessories = get_items(items, "Accessory", occasion)

        # If we run out of core clothing components, stop trying to build outfits
        if not (dresses or (tops and bottoms)):
            break

        current_outfits = []

        # -----------------------------
        # Dress Based Outfits
        # -----------------------------
        for dress in dresses:
            shoe = choose_best_shoes(shoes, dress=dress, occasion=occasion)
            bag = choose_best_bag(bags, shoe, occasion)
            accessory = choose_best_accessory(accessories, bag, occasion)

            score, breakdown = score_outfit(
                dress=dress, shoes=shoe, bag=bag, accessory=accessory,
                occasion=occasion, weather=weather, style=style, color=color,
            )

            current_outfits.append({
                "Dress": dress, "Shoes": shoe, "Bag": bag, "Accessory": accessory,
                "score": score, "breakdown": breakdown,
            })

        # -----------------------------
        # Top + Bottom Outfits
        # -----------------------------
        for top, bottom in itertools.product(tops, bottoms):
            shoe = choose_best_shoes(shoes, top=top, bottom=bottom, occasion=occasion)
            bag = choose_best_bag(bags, shoe, occasion)
            accessory = choose_best_accessory(accessories, bag, occasion)

            score, breakdown = score_outfit(
                top=top, bottom=bottom, shoes=shoe, bag=bag, accessory=accessory,
                occasion=occasion, weather=weather, style=style, color=color,
            )

            current_outfits.append({
                "Top": top, "Bottom": bottom, "Shoes": shoe, "Bag": bag, "Accessory": accessory,
                "score": score, "breakdown": breakdown,
            })

        # If no valid outfits could be made from the remaining clothes, stop
        if not current_outfits:
            break

        # Sort the outfits generated in THIS loop by score
        current_outfits.sort(key=lambda x: x["score"], reverse=True)
        
        # Take the absolute best outfit
        best_outfit = current_outfits[0]
        final_outfits.append(best_outfit)

        # ----------------------------------
        # STRICT UNIQUENESS: Remove used items
        # ----------------------------------
        # Get all the items we just used in this winning outfit
        used_items = [
            best_outfit.get("Top"), best_outfit.get("Bottom"), best_outfit.get("Dress"),
            best_outfit.get("Shoes"), best_outfit.get("Bag"), best_outfit.get("Accessory")
        ]
        
        # Get their unique memory IDs (ignoring None values if no bag/accessory was picked)
        used_ids = {id(item) for item in used_items if item is not None}
        
        # Filter the master `items` list! 
        # When the loop runs again, these items physically will not exist in the pool,
        # forcing the selectors to pick completely new shoes, bags, and clothes.
        items = [item for item in items if id(item) not in used_ids]


    # ----------------------------------
    # Generate explanation + shopping query
    # ----------------------------------
    for outfit in final_outfits:

        outfit["reason"] = build_reason(outfit)
        search_parts = []

        for key, item in outfit.items():
            if key in ["score", "breakdown", "reason"]:
                continue
            if not item:
                continue
            
            search_parts.append(item.name)

        outfit["search_query"] = " ".join(search_parts)

        # -------- Better shopping suggestions --------
        keywords = []

        if style: keywords.append(style)
        if color: keywords.append(color)
        if occasion: keywords.append(occasion)
        
        if outfit.get("Shoes"): keywords.append("Shoes")
        if outfit.get("Bag"): keywords.append("Bag")
        if outfit.get("Accessory"): keywords.append("Watch")

        outfit["shopping_query"] = " ".join(keywords)

    return final_outfits