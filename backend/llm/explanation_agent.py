import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv


# Load environment variables from backend/.env so Gemini key is available locally
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


def _load_model() -> genai.GenerativeModel:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable."
        )

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


model = _load_model()

def generate_explanation(label_data, mode="general"):
    prompt = f"""
You are a food safety and nutrition assistant.

Given the following extracted facts, explain clearly and factually.
Do NOT give medical advice.

Nutrition per 100g:
{label_data["nutrition_normalized"]["nutrition_per_100g"]}

Ingredients:
{label_data["semantic_ingredients"]["canonical_ingredients"]}

Additives:
{label_data["semantic_ingredients"]["additives"]}

Health score:
{label_data["health"]["health_score"]} ({label_data["health"]["health_category"]})

User mode:
{mode}

Explain:
• Is this good or bad?
• Why?
• Who should avoid it?
• When can it be consumed?
"""

    response = model.generate_content(prompt)
    return response.text
