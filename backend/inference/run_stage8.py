from inference.food_priors import FOOD_PRIORS
from inference.macro_estimator import estimate_calories, midpoint
from inference.uncertainty_model import confidence_from_range

def run_stage8(nutrition_per_100g, semantic_ingredients):
    inferred = {}

    # Infer food category
    category = "biscuit" if "chocolate" in semantic_ingredients["canonical_ingredients"] else "snack"
    priors = FOOD_PRIORS[category]

    # Carbohydrates
    if nutrition_per_100g.get("carbohydrate_g") is None:
        low, high = priors["carbohydrate_g"]
        inferred["carbohydrate_g"] = {
            "value": midpoint(low, high),
            "confidence": confidence_from_range(low, high),
            "source": "statistical_estimate"
        }

    # Sugars
    if nutrition_per_100g.get("sugars_g") is None:
        low, high = priors["sugars_g"]
        inferred["sugars_g"] = {
            "value": midpoint(low, high),
            "confidence": confidence_from_range(low, high),
            "source": "statistical_estimate"
        }

    # Protein
    if nutrition_per_100g.get("protein_g") is None:
        low, high = priors["protein_g"]
        inferred["protein_g"] = {
            "value": midpoint(low, high),
            "confidence": confidence_from_range(low, high),
            "source": "statistical_estimate"
        }

    # Calories (energy-consistent)
    if nutrition_per_100g.get("calories") is None:
        fat = nutrition_per_100g.get("fat_g")
        carbs = inferred.get("carbohydrate_g", {}).get("value")
        protein = inferred.get("protein_g", {}).get("value")

        calories = estimate_calories(fat, carbs, protein)
        if calories:
            inferred["calories"] = {
                "value": calories,
                "confidence": 0.65,
                "source": "macro_energy_estimate"
            }

    return inferred
