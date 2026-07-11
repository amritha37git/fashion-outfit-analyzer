import random

INTRO = [

    "This outfit creates a balanced and stylish appearance.",

    "The selected pieces work beautifully together.",

    "This combination provides a clean and fashionable look.",

    "These wardrobe pieces complement each other perfectly.",

    "This outfit offers a modern and well-balanced style."

]

ENDING = [

    "It is well suited for your selected occasion.",

    "The colors are coordinated for a pleasant overall appearance.",

    "The outfit is comfortable while maintaining a stylish look.",

    "The selected accessories complete the outfit naturally.",

    "The combination works well for the chosen weather."

]


def build_reason(outfit):

    intro = random.choice(INTRO)

    ending = random.choice(ENDING)

    if outfit.get("Dress"):

        return (
            f"{intro} "
            f"The {outfit['Dress'].name} acts as the main statement piece. "
            f"{ending}"
        )

    return (
        f"{intro} "
        f"The {outfit['Top'].name} pairs nicely with "
        f"{outfit['Bottom'].name}. "
        f"{ending}"
    )