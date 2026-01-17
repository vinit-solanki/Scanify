from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class NutritionPer100g(BaseModel):
    """Nutrition facts normalized to per 100g"""
    calories: Optional[float] = None
    fat_g: Optional[float] = None
    saturated_fat_g: Optional[float] = None
    trans_fat_g: Optional[float] = None
    cholesterol_mg: Optional[float] = None
    sodium_mg: Optional[float] = None
    carbohydrate_g: Optional[float] = None
    dietary_fiber_g: Optional[float] = None
    sugars_g: Optional[float] = None
    protein_g: Optional[float] = None


class NutritionNormalized(BaseModel):
    """Nutrition facts with serving size and per 100g breakdown"""
    serving_size_g: Optional[float] = None
    serving_size_description: Optional[str] = None
    nutrition_per_serving: Optional[Dict[str, Any]] = None
    nutrition_per_100g: Optional[NutritionPer100g] = None


class SemanticIngredients(BaseModel):
    """Semantic analysis of ingredients"""
    raw_ingredients: List[str] = Field(default_factory=list)
    canonical_ingredients: List[str] = Field(default_factory=list)
    allergens: List[str] = Field(default_factory=list)
    additives: List[str] = Field(default_factory=list)
    processing_indicators: List[str] = Field(default_factory=list)


class HealthAnalysis(BaseModel):
    """Health score and analysis"""
    health_score: float = 50.0
    health_category: str = "Unknown"  # Excellent, Good, Fair, Poor
    penalties: Dict[str, float] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    """Complete analysis result that matches frontend expectations"""
    is_valid: bool = True
    mode: str = "general"  # general, diabetes, weight_loss
    
    # Text processing
    raw_text: str = ""
    
    # Ingredients analysis
    semantic_ingredients: Optional[SemanticIngredients] = None
    
    # Nutrition analysis
    nutrition_normalized: Optional[NutritionNormalized] = None
    
    # Health analysis
    health: Optional[HealthAnalysis] = None
    
    # Confidence and explanation
    overall_confidence: float = 0.5
    explanation: str = ""
    
    # Metadata
    error_message: Optional[str] = None
