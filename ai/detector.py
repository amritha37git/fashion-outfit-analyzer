import os
import json
import time

from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


DEFAULT_RESULT = {

    "name": "Unknown Item",

    "category": "Top",

    "brand": "Unknown",

    "color": "Unknown",

    "season": "All Season",

    "occasion": "Casual",

    "description": "AI is temporarily unavailable. Please edit the details manually."
}


VALID_CATEGORIES = [

    "Top",
    "Bottom",
    "Dress",
    "Shirt",
    "T-shirt",
    "Hoodie",
    "Jacket",
    "Shoes",
    "Bag",
    "Accessory"

]


VALID_SEASONS = [

    "Summer",
    "Winter",
    "Rainy",
    "All Season"

]


VALID_OCCASIONS = [

    "Casual",
    "College",
    "Office",
    "Party",
    "Wedding"

]


def clean_result(result):

    for key, value in DEFAULT_RESULT.items():

        result.setdefault(key, value)

    result["name"] = result["name"].title()

    result["brand"] = result["brand"].title()

    result["color"] = result["color"].title()

    if result["category"] not in VALID_CATEGORIES:

        result["category"] = "Top"

    if result["season"] not in VALID_SEASONS:

        result["season"] = "All Season"

    if result["occasion"] not in VALID_OCCASIONS:

        result["occasion"] = "Casual"

    return result


def optimize_image(image_path):

    image = Image.open(image_path)

    image.thumbnail((1024, 1024))

    return image


def analyze_image(image_path):

    image = optimize_image(image_path)

    prompt = """
You are an expert AI Fashion Stylist.

Analyze ONLY the clothing item shown.

Return ONLY valid JSON.

{

"name":"",

"category":"",

"brand":"",

"color":"",

"season":"",

"occasion":"",

"description":""

}

Rules:

Name:
Short clothing name.

Category:
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
Unknown if logo not visible.

Color:
Only dominant color.

Season:
Summer
Winter
Rainy
All Season

Occasion:
Casual
College
Office
Party
Wedding

Description:
One short sentence.

Return ONLY JSON.

No markdown.

No explanations.
"""

    MAX_RETRIES = 3

    for attempt in range(MAX_RETRIES):

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

            return clean_result(result)

        except json.JSONDecodeError:

            print("Gemini returned invalid JSON.")

            if attempt == MAX_RETRIES - 1:

                return DEFAULT_RESULT.copy()

        except Exception as e:

            print(f"Attempt {attempt+1} failed:", e)

            if "503" in str(e):

                time.sleep(3)

                continue

            if "429" in str(e):

                return {

                    **DEFAULT_RESULT,

                    "description": "Daily AI quota exceeded. Please try again tomorrow."

                }

            if attempt == MAX_RETRIES - 1:

                return DEFAULT_RESULT.copy()

    return DEFAULT_RESULT.copy()