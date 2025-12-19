from health.thresholds import THRESHOLDS

def score_nutrient(value, low, high):
    if value is None:
        return 0

    if value <= low:
        return 0
    elif value >= high:
        return 1
    else:
        return (value - low) / (high - low)


def compute_health_score(nutrition, semantic_ingredients, mode="general"):
    penalties = {}
    score = 100

    # Nutrient penalties
    for nutrient, limits in THRESHOLDS.items():
        value = nutrition.get(nutrient)
        penalty = score_nutrient(value, limits["low"], limits["high"])
        penalties[nutrient] = round(penalty, 2)
        score -= penalty * 20

    # Additive penalty
    score -= len(semantic_ingredients["additives"]) * 5

    # Processing penalty
    score -= len(semantic_ingredients["processing_indicators"]) * 7

    # Diabetes mode
    if mode == "diabetes":
        if nutrition.get("sugars_g", 0) and nutrition["sugars_g"] > 10:
            score -= 15

    # Weight-loss mode
    if mode == "weight_loss":
        if nutrition.get("calories", 0) and nutrition["calories"] > 400:
            score -= 10

    score = max(0, round(score))

    category = (
        "Safe"
        if score >= 80 else
        "Nominal"
        if score >= 50 else
        "Harmful"
    )

    return {
        "health_score": score,
        "health_category": category,
        "penalties": penalties
    }
