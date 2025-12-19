def classify_product(features, user_profile):
    mode = user_profile.get("goal", "general")

    nutrition = features["nutrition_per_100g"]
    ingredients = features["ingredients"]

    score = 100
    reasons = []

    sugar = nutrition.get("sugar_g")
    fiber = nutrition.get("fiber_g")
    sat_fat = nutrition.get("saturated_fat_g")

    # Indian thresholds
    if sugar and sugar > 25:
        score -= 60
        reasons.append("very_high_sugar")

    if sat_fat and sat_fat > 5:
        score -= 20
        reasons.append("high_saturated_fat")

    if fiber and fiber < 3:
        score -= 15
        reasons.append("low_fiber")

    if ingredients.get("refined_flour"):
        score -= 10
        reasons.append("refined_flour")

    # Mode-specific overrides
    if mode == "diabetes" and sugar and sugar > 10:
        return {
            "health_category": "Harmful",
            "health_score": 0,
            "mode": mode,
            "reasons": reasons + ["unsafe_for_diabetes"]
        }

    if mode == "weight_loss" and (fiber and fiber < 3):
        score -= 20
        reasons.append("poor_satiety")

    # Final category
    if score <= 30:
        category = "Harmful"
    elif score <= 60:
        category = "Nominal"
    else:
        category = "Safe"

    return {
        "health_category": category,
        "health_score": max(score, 0),
        "mode": mode,
        "reasons": reasons
    }
