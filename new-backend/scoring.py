from typing import Dict, List, Tuple, Optional


def _get(d: Dict[str, float], key: str, default: float = 0.0) -> float:
    val = d.get(key)
    try:
        return float(val) if val is not None else default
    except Exception:
        return default


def _get_health_category(score: float) -> str:
    """Categorize health score into meaningful categories."""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    else:
        return "Poor"


def score(
    nutrition: Dict[str, float], 
    tags: List[str], 
    mode: str = "weight_loss"
) -> Tuple[float, List[Dict[str, str]], Dict[str, float]]:
    """
    Score product on health based on nutrition and tags.
    Returns (score_out_of_100, reasons, penalties_dict).
    """
    reasons: List[Dict[str, str]] = []
    penalties: Dict[str, float] = {}
    score = 100.0

    calories = _get(nutrition, "calories")
    fat = _get(nutrition, "total_fat_g")
    sat_fat = _get(nutrition, "saturated_fat_g")
    carbs = _get(nutrition, "carbohydrate_g")
    sugars = _get(nutrition, "sugars_g")
    fiber = _get(nutrition, "dietary_fiber_g")
    protein = _get(nutrition, "protein_g")
    sodium_mg = _get(nutrition, "sodium_mg")

    if mode == "diabetes":
        # Sugars are the main concern
        if sugars > 20:
            penalty = 40
            score -= penalty
            penalties["high_sugars"] = penalty
            reasons.append({"metric": "sugars_g", "reason": f">20g sugars (found {sugars}g)"})
        elif sugars > 10:
            penalty = 25
            score -= penalty
            penalties["high_sugars"] = penalty
            reasons.append({"metric": "sugars_g", "reason": f">10g sugars (found {sugars}g)"})
        elif sugars > 5:
            penalty = 10
            score -= penalty
            penalties["high_sugars"] = penalty
            reasons.append({"metric": "sugars_g", "reason": f">5g sugars (found {sugars}g)"})

        # Carbs matter
        if carbs > 40:
            penalty = 25
            score -= penalty
            penalties["high_carbs"] = penalty
            reasons.append({"metric": "carbs", "reason": f">40g carbs (found {carbs}g)"})
        elif carbs > 30:
            penalty = 15
            score -= penalty
            penalties["high_carbs"] = penalty
            reasons.append({"metric": "carbs", "reason": f">30g carbs (found {carbs}g)"})

        # Fiber is beneficial
        if fiber < 1:
            penalty = 20
            score -= penalty
            penalties["low_fiber"] = penalty
            reasons.append({"metric": "fiber", "reason": f"<1g fiber (found {fiber}g)"})
        elif fiber < 3:
            penalty = 10
            score -= penalty
            penalties["low_fiber"] = penalty
            reasons.append({"metric": "fiber", "reason": f"<3g fiber (found {fiber}g)"})

        # Tag penalties
        if "high_sugar" in tags:
            penalty = 10
            score -= penalty
            penalties["sugar_ingredients"] = penalty
            reasons.append({"metric": "tags", "reason": "high_sugar ingredients"})

        if sodium_mg > 600:
            penalty = 10
            score -= penalty
            penalties["high_sodium"] = penalty
            reasons.append({"metric": "sodium", "reason": f">600mg sodium (found {sodium_mg}mg)"})
        
        if sat_fat > 10:
            penalty = 10
            score -= penalty
            penalties["high_sat_fat"] = penalty
            reasons.append({"metric": "sat_fat", "reason": f">10g saturated fat (found {sat_fat}g)"})

    else:  # weight_loss (default)
        # Calories are the main concern
        if calories > 400:
            penalty = 30
            score -= penalty
            penalties["high_calories"] = penalty
            reasons.append({"metric": "calories", "reason": f">400 kcal (found {calories})"})
        elif calories > 250:
            penalty = 20
            score -= penalty
            penalties["high_calories"] = penalty
            reasons.append({"metric": "calories", "reason": f">250 kcal (found {calories})"})
        elif calories > 150:
            penalty = 10
            score -= penalty
            penalties["high_calories"] = penalty
            reasons.append({"metric": "calories", "reason": f">150 kcal (found {calories})"})

        # Fat content
        if fat > 20:
            penalty = 25
            score -= penalty
            penalties["high_fat"] = penalty
            reasons.append({"metric": "fat", "reason": f">20g fat (found {fat}g)"})
        elif fat > 15:
            penalty = 15
            score -= penalty
            penalties["high_fat"] = penalty
            reasons.append({"metric": "fat", "reason": f">15g fat (found {fat}g)"})

        # Sugars
        if sugars > 15:
            penalty = 20
            score -= penalty
            penalties["high_sugars"] = penalty
            reasons.append({"metric": "sugars", "reason": f">15g sugars (found {sugars}g)"})
        elif sugars > 8:
            penalty = 10
            score -= penalty
            penalties["high_sugars"] = penalty
            reasons.append({"metric": "sugars", "reason": f">8g sugars (found {sugars}g)"})

        # Positive factors
        if protein < 8:
            penalty = 10
            score -= penalty
            penalties["low_protein"] = penalty
            reasons.append({"metric": "protein", "reason": f"<8g protein (found {protein}g)"})
        
        if fiber < 3:
            penalty = 10
            score -= penalty
            penalties["low_fiber"] = penalty
            reasons.append({"metric": "fiber", "reason": f"<3g fiber (found {fiber}g)"})
        
        if "refined_grains" in tags:
            penalty = 10
            score -= penalty
            penalties["refined_grains"] = penalty
            reasons.append({"metric": "tags", "reason": "refined grains"})

    # Ensure score is within bounds
    if score < 0:
        score = 0.0
    elif score > 100:
        score = 100.0

    return round(score, 1), reasons, penalties


def analyze_health(
    nutrition: Dict[str, float],
    tags: List[str],
    mode: str = "weight_loss"
) -> Dict:
    """Generate comprehensive health analysis."""
    score_value, risk_reasons, penalties = score(nutrition, tags, mode)
    health_category = _get_health_category(score_value)
    
    recommendations = []
    if score_value < 40:
        if mode == "diabetes":
            recommendations.append("Reduce sugar and carbohydrate intake significantly")
        else:
            recommendations.append("This is a high-calorie product; consider portion control")
    
    if "high_fat" in penalties or "high_sat_fat" in penalties:
        recommendations.append("Consider lower-fat alternatives")
    
    if "low_fiber" in penalties:
        recommendations.append("Choose products with more dietary fiber")
    
    if "low_protein" in penalties:
        recommendations.append("Look for products with more protein")
    
    if not recommendations:
        recommendations.append("Good nutritional profile")
    
    return {
        "health_score": score_value,
        "health_category": health_category,
        "penalties": penalties,
        "recommendations": recommendations,
    }
