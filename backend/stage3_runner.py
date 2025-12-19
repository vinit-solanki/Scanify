from ontology.ingredient_cleaner import clean_ingredient_text
from intelligence.intelligence_classifier import classify_ingredients

def run_stage3(ingredient_output):
    raw_text = ingredient_output["raw_text"]

    cleaned_text = clean_ingredient_text(raw_text)

    classification = classify_ingredients(cleaned_text)

    confidence = min(
        1.0,
        ingredient_output["confidence"] / 100 + 0.1
    )

    classification["confidence"] = round(confidence, 2)

    return classification
