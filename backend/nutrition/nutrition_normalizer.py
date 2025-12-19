def normalize_nutrition(raw_nutrition):
    """
    Converts extracted nutrition into numeric form.
    """

    normalized = {}

    def to_float(v):
        try:
            return float(v)
        except:
            return None

    normalized["calories"] = to_float(raw_nutrition.get("calories"))
    normalized["fat_g"] = to_float(raw_nutrition.get("total_fat"))
    normalized["saturated_fat_g"] = to_float(raw_nutrition.get("saturated_fat"))
    normalized["carbohydrate_g"] = to_float(raw_nutrition.get("carbohydrate"))
    normalized["sugars_g"] = to_float(raw_nutrition.get("sugars"))
    normalized["protein_g"] = to_float(raw_nutrition.get("protein"))
    normalized["sodium_mg"] = to_float(raw_nutrition.get("sodium"))

    return normalized
