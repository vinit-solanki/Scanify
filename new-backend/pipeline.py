from typing import Dict, Optional
import logging

import ocr
import extract
import ontology
import scoring
import llm
from schemas import (
    NutritionPer100g,
    NutritionNormalized,
    SemanticIngredients,
    HealthAnalysis,
    AnalysisResult,
)

logger = logging.getLogger(__name__)


def _normalize_mode(mode: str) -> str:
    """Normalize mode to one of: diabetes, weight_loss, general."""
    m = (mode or "").lower().strip()
    if m in ("diabetes", "weight_loss"):
        return m
    return "weight_loss"


def analyze_text(label_text: str, mode: str = "general") -> Dict:
    """Analyze nutrition label text."""
    try:
        normalized_mode = _normalize_mode(mode)
        text = (label_text or "").strip()
        
        if not text:
            return _invalid_result("No text provided for analysis")
        
        # Parse ingredients and nutrition
        ingredients = extract.parse_ingredients(text)
        nutrition_dict = extract.parse_nutrition(text)
        
        # If we couldn't extract any meaningful data, mark as invalid
        if not ingredients and not nutrition_dict:
            return _invalid_result("Could not extract ingredients or nutrition information")
        
        # Semantic ingredient analysis
        allergens = ontology.detect_allergens(ingredients)
        additives = ontology.detect_additives(ingredients)
        processing = ontology.detect_processing_indicators(ingredients)
        tags = sorted(list(ontology.tag_ingredients(ingredients)))
        
        # Normalize nutrition to per 100g
        serving_size_g = nutrition_dict.get("serving_size_g")
        nutrition_per_100g_dict = extract.normalize_nutrition_to_per_100g(
            nutrition_dict, serving_size_g
        )
        
        # Create nutrition objects
        nutrition_per_100g = NutritionPer100g(
            calories=nutrition_per_100g_dict.get("calories"),
            fat_g=nutrition_per_100g_dict.get("total_fat_g"),
            saturated_fat_g=nutrition_per_100g_dict.get("saturated_fat_g"),
            trans_fat_g=nutrition_per_100g_dict.get("trans_fat_g"),
            cholesterol_mg=nutrition_per_100g_dict.get("cholesterol_mg"),
            sodium_mg=nutrition_per_100g_dict.get("sodium_mg"),
            carbohydrate_g=nutrition_per_100g_dict.get("carbohydrate_g"),
            dietary_fiber_g=nutrition_per_100g_dict.get("dietary_fiber_g"),
            sugars_g=nutrition_per_100g_dict.get("sugars_g"),
            protein_g=nutrition_per_100g_dict.get("protein_g"),
        )
        
        nutrition_normalized = NutritionNormalized(
            serving_size_g=serving_size_g,
            serving_size_description=nutrition_dict.get("serving_size_description"),
            nutrition_per_serving=nutrition_dict,
            nutrition_per_100g=nutrition_per_100g,
        )
        
        # Health analysis and scoring
        health_analysis_dict = scoring.analyze_health(
            nutrition_per_100g_dict, tags, normalized_mode
        )
        health = HealthAnalysis(**health_analysis_dict)
        
        # Generate explanation
        explanation = llm.generate_explanation(
            {
                "ingredients": ingredients,
                "nutrition": nutrition_dict,
                "nutrition_per_100g": nutrition_per_100g_dict,
                "tags": tags,
                "allergens": allergens,
                "additives": additives,
                "risks": health_analysis_dict.get("recommendations", []),
                "score": health.health_score,
                "health_category": health.health_category,
            },
            normalized_mode,
        )
        
        # Semantic ingredients
        semantic_ingredients = SemanticIngredients(
            raw_ingredients=ingredients,
            canonical_ingredients=ingredients[:10],  # Top 10
            allergens=allergens,
            additives=additives,
            processing_indicators=processing,
        )
        
        # Overall confidence based on data completeness
        confidence = _calculate_confidence(nutrition_dict, ingredients)
        
        result = AnalysisResult(
            is_valid=True,
            mode=normalized_mode,
            raw_text=text,
            semantic_ingredients=semantic_ingredients,
            nutrition_normalized=nutrition_normalized,
            health=health,
            overall_confidence=confidence,
            explanation=explanation,
        )
        
        return result.model_dump()
    
    except Exception as e:
        logger.error(f"Error in analyze_text: {str(e)}", exc_info=True)
        return _invalid_result(f"Analysis error: {str(e)}")


def analyze_image(file_bytes: bytes, mode: str = "general") -> Dict:
    """Analyze food label from image using OCR."""
    try:
        if not file_bytes:
            return _invalid_result("No image data provided")
        
        text = ocr.extract_text(file_bytes)
        
        if not text or text.strip() == "":
            return _invalid_result("Could not extract text from image. Please ensure the image is clear and contains a nutrition label.")
        
        return analyze_text(text, mode=mode)
    
    except Exception as e:
        logger.error(f"Error in analyze_image: {str(e)}", exc_info=True)
        return _invalid_result(f"Image analysis error: {str(e)}")


def _calculate_confidence(nutrition_dict: Dict, ingredients: list) -> float:
    """Calculate analysis confidence based on data completeness."""
    confidence = 0.5
    
    # More nutrients extracted = higher confidence
    nutrient_keys = [k for k in nutrition_dict.keys() if k not in ("serving_size_g", "serving_size_description")]
    if len(nutrient_keys) >= 5:
        confidence += 0.25
    elif len(nutrient_keys) >= 3:
        confidence += 0.15
    
    # More ingredients extracted = higher confidence
    if len(ingredients) >= 5:
        confidence += 0.2
    elif len(ingredients) >= 3:
        confidence += 0.1
    
    # Serving size info helps
    if "serving_size_g" in nutrition_dict:
        confidence += 0.05
    
    return min(round(confidence, 2), 1.0)


def _invalid_result(error_message: str) -> Dict:
    """Return an invalid analysis result with error message."""
    result = AnalysisResult(
        is_valid=False,
        error_message=error_message,
    )
    return result.model_dump()
