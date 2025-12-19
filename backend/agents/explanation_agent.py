import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_explanation(features, classification, user_profile):
    prompt = """
You are a nutrition assistant for Indian consumers.

User goal: {goal}
Health category: {category}
Health score: {score}

Features:
{features}

Explain clearly:
- Summary
- Is it good for me?
- When to eat
- Who should avoid
- Final advice

Return ONLY valid JSON:
{schema}
""".format(
        goal=classification["mode"],
        category=classification["health_category"],
        score=classification["health_score"],
        features=json.dumps(features, indent=2),
        schema="""
{
  "summary": "",
  "is_it_good_for_me": "",
  "when_to_eat": "",
  "who_should_avoid": "",
  "final_advice": "",
  "context_note": ""
}
"""
    )

    response = model.generate_content(prompt)
    return json.loads(response.text)
