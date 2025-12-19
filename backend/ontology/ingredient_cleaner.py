import re

def clean_ingredient_text(text):
    text = text.lower()

    # Remove vitamins & minerals
    text = re.sub(
        r"(iron|riboflavin|niacin|vitamin|folic acid|calcium)",
        "",
        text
    )

    # Remove garbage tokens
    text = re.sub(r"\b(an|og|i fat)\b", "", text)

    # Normalize separators
    text = text.replace(".", ",")
    text = re.sub(r"\s+", " ", text)

    return text.strip()
