import re
from table.row_clusterer import cluster_rows
from text_utils.text_utils import normalize_text

def parse_nutrition_table(blocks):
    rows = cluster_rows(blocks)

    nutrition = {}

    for row in rows:
        row_text = " ".join(normalize_text(b["text"]) for b in row)

        # Calories
        if "calorie" in row_text or "energy" in row_text:
            match = re.search(r"(\d+)", row_text)
            if match:
                nutrition["calories"] = float(match.group(1))

        # Fat
        if "fat" in row_text and "saturated" not in row_text:
            match = re.search(r"(\d+\.?\d*)\s*g", row_text)
            if match:
                nutrition["fat_g"] = float(match.group(1))

        # Saturated Fat
        if "saturated" in row_text:
            match = re.search(r"(\d+\.?\d*)\s*g", row_text)
            if match:
                nutrition["saturated_fat_g"] = float(match.group(1))

        # Carbohydrate
        if "carbohydrate" in row_text:
            match = re.search(r"(\d+\.?\d*)\s*g", row_text)
            if match:
                nutrition["carbohydrate_g"] = float(match.group(1))

        # Sugars
        if "sugar" in row_text:
            match = re.search(r"(\d+\.?\d*)\s*g", row_text)
            if match:
                nutrition["sugars_g"] = float(match.group(1))

        # Sodium
        if "sodium" in row_text:
            match = re.search(r"(\d+)\s*mg", row_text)
            if match:
                nutrition["sodium_mg"] = float(match.group(1))

        # Protein
        if "protein" in row_text:
            match = re.search(r"(\d+\.?\d*)\s*g", row_text)
            if match:
                nutrition["protein_g"] = float(match.group(1))

    return nutrition
