def build_label_schema(
    ingredient_result,
    nutrition_result,
    validation_result
):
    return {
        "is_valid": validation_result["is_valid_label"],
        "ingredients": ingredient_result,
        "nutrition": nutrition_result,
        "overall_confidence": round(
            (
                ingredient_result["confidence"] +
                nutrition_result["confidence"]
            ) / 2,
            2
        )
    }
