from nutrition.serving_size_inferer import infer_serving_size
from nutrition.nutrition_normalizer import normalize_nutrition
from nutrition.nutrition_inference import infer_per_100g

def run_stage4(nutrition_output, text_blocks):
    serving_size, serving_conf = infer_serving_size(text_blocks)

    normalized = normalize_nutrition(nutrition_output["nutrition"])
    per_100g = infer_per_100g(normalized, serving_size)

    confidence = round(
        (nutrition_output["confidence"] / 100 + serving_conf) / 2,
        2
    )

    return {
        "nutrition_per_100g": per_100g,
        "serving_size_g": serving_size,
        "inference_confidence": confidence
    }
