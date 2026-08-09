import os
import json

from dotenv import load_dotenv
from google import genai
from PIL import Image


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def detect_season(data):

    text = (
        data.get("description", "")
        +
        data.get("fabric", "")
        +
        data.get("style", "")
    ).lower()

    if any(word in text for word in [
        "wool",
        "sweater",
        "jacket",
        "coat",
        "thick",
        "thermal"
    ]):
        return "Winter"

    if any(word in text for word in [
        "raincoat",
        "waterproof",
        "windbreaker"
    ]):
        return "Rainy"

    if any(word in text for word in [
        "cotton",
        "linen",
        "short",
        "sleeveless",
        "light",
        "chiffon"
    ]):
        return "Summer"

    return "All Season"


def analyze_image(image_path):

    image = Image.open(image_path)

    prompt = """

You are an AI fashion expert.

Analyze this clothing image.

Return ONLY valid JSON.

Format:

{
"name":"",
"category":"",
"brand":"",
"color":"",
"fabric":"",
"sleeves":"",
"style":"",
"occasion":"",
"description":""
}

Rules:

Category must be exactly one of:

Top
Bottom
Dress
Shirt
T-shirt
Hoodie
Jacket
Shoes
Bag
Accessory

Brand:

If no visible logo or brand name,
return:
Unknown

Color:

Return only the dominant color.

Occasion:

Choose ONLY ONE:

Casual
College
Office
Party
Wedding

Fabric:

Estimate the fabric if possible.

Sleeves:

Choose ONLY ONE:

Short
Long
Sleeveless

Style:

Choose ONLY ONE from the following values:

Casual
Formal
Business Casual
Party
Traditional
Streetwear
Sporty
Minimalist
Elegant
Vintage
Bohemian

Return exactly one value.

Description:

Write one short sentence describing the clothing item.

Return ONLY the JSON object.
Do NOT use markdown.
Do NOT add explanations.

"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=[
                prompt,
                image
            ]
        )

        text = response.text.strip()

        text = (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        result = json.loads(text)

        result.setdefault(
            "name",
            "Unknown Item"
        )

        result.setdefault(
            "brand",
            "Unknown"
        )

        result.setdefault(
            "color",
            "Unknown"
        )

        result.setdefault(
            "occasion",
            "Casual"
        )

        result.setdefault(
            "style",
            "Casual"
        )

        result.setdefault(
            "description",
            ""
        )

        # Detect season automatically
        result["season"] = detect_season(result)

        return result

    except Exception as e:

        print("Gemini Error:", e)

        return {

            "name": "Unknown Item",

            "category": "Top",

            "brand": "Unknown",

            "color": "Unknown",

            "season": "All Season",

            "occasion": "Casual",

            "style": "Casual",

            "description": "AI unavailable"

        }