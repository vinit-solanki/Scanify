from vision.ocr_agent import extract_text_blocks
from validation.label_validator import validate_food_label
from extraction.layout_analyzer import analyze_layout
from extraction.ingredient_extractor import extract_ingredients
from extraction.nutrition_extractor import extract_nutrition
from schemas.label_schema import build_label_schema

from stage3_runner import run_stage3
from nutrition.run_stage4 import run_stage4
from health.scoring_engine import compute_health_score
from llm.explanation_agent import generate_explanation

from table.run_stage7 import run_stage7
from inference.run_stage8 import run_stage8

IMAGE_PATH = "data/oreo_label.jpg"
USER_MODE = "general"  # general | diabetes | weight_loss

def main():
    text_blocks = extract_text_blocks(IMAGE_PATH)

    validation = validate_food_label(text_blocks)
    if not validation["is_valid_label"]:
        print("Invalid food label")
        return

    layout = analyze_layout(text_blocks)

    ingredients = extract_ingredients(layout["ingredient_blocks"])
    nutrition = extract_nutrition(layout["nutrition_blocks"])

    label_data = build_label_schema(
        ingredients,
        nutrition,
        validation
    )

    # Stage-3
    label_data["semantic_ingredients"] = run_stage3(
        label_data["ingredients"]
    )

    # Stage-4
    label_data["nutrition_normalized"] = run_stage4(
        label_data["nutrition"],
        text_blocks
    )

    # Stage-5
    label_data["health"] = compute_health_score(
        label_data["nutrition_normalized"]["nutrition_per_100g"],
        label_data["semantic_ingredients"],
        mode=USER_MODE
    )

    # Stage-6
    label_data["explanation"] = generate_explanation(
        label_data,
        mode=USER_MODE
    )

    print("\nFINAL OUTPUT:\n")
    print(label_data)

    # Stage-7: Table reconstruction
    table_nutrition = run_stage7(text_blocks)

    # Merge with Stage-4 inference
    label_data["nutrition_normalized"]["nutrition_per_100g"].update(
        {k: v for k, v in table_nutrition.items() if v is not None}
    )

    # Stage-8: Statistical nutrition inference
    estimated_nutrition = run_stage8(
        label_data["nutrition_normalized"]["nutrition_per_100g"],
        label_data["semantic_ingredients"]
    )

    label_data["nutrition_estimated"] = estimated_nutrition


if __name__ == "__main__":
    main()
