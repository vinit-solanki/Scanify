import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def extract_features(text):
    """
    Uses Gemini to convert label text into structured JSON
    """

    prompt = """
You are a food label extraction agent for Indian packaged foods.

Extract ingredients, allergens, and nutrition per 100g.

TEXT:
{text}

Return ONLY valid JSON:
{schema}
""".format(
        text=text,
        schema="""
{
  "ingredients": {
    "sugar": true,
    "palm_oil": true,
    "refined_flour": true,
    "artificial_sweeteners": false,
    "preservatives": false
  },
  "allergens": [],
  "nutrition_per_100g": {
    "calories": null,
    "sugar_g": null,
    "fat_g": null,
    "saturated_fat_g": null,
    "protein_g": null,
    "fiber_g": null,
    "sodium_mg": null
  }
}
"""
    )

    response = model.generate_content(prompt)

    return json.loads(response.text)
