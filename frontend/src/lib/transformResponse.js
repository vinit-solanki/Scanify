/**
 * Transform backend nutrition analysis response to ProductScan component format
 */
export function transformAnalysisToScanResult(data) {
  if (!data || !data.is_valid) {
    throw new Error("Invalid or unrecognized food label");
  }

  const { health, semantic_ingredients, nutrition_normalized, explanation, overall_confidence } = data;
  const confidenceRaw = Number(overall_confidence);
  const confidence = Number.isFinite(confidenceRaw)
    ? Math.max(0, Math.min(100, Math.round(confidenceRaw <= 1 ? confidenceRaw * 100 : confidenceRaw)))
    : 0;

  // Build category from health category
  const category = health?.health_category || "Unknown";
  
  // Build labels from various sources
  const labels = [];
  
  // Add processing indicators
  if (semantic_ingredients?.processing_indicators?.length > 0) {
    labels.push(...semantic_ingredients.processing_indicators.map(p => 
      p.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
    ));
  }
  
  // Add allergen info
  if (semantic_ingredients?.allergens?.length > 0) {
    labels.push(`Contains: ${semantic_ingredients.allergens.join(', ')}`);
  }
  
  // Add additive count
  if (semantic_ingredients?.additives?.length > 0) {
    labels.push(`${semantic_ingredients.additives.length} Additives`);
  }

  // If no labels, add a default
  if (labels.length === 0) {
    labels.push("Processed Food");
  }

  // Build attributes from nutrition data
  const attributes = {
    "Health Category": category,
    "Health Score": `${health?.health_score || 0}/100`,
    "Serving Size": nutrition_normalized?.serving_size_description
      || (nutrition_normalized?.serving_size_g != null ? `${nutrition_normalized.serving_size_g}g` : "Unknown")
  };

  // Add key nutrition facts if available
  if (nutrition_normalized?.nutrition_per_100g) {
    const nutr = nutrition_normalized.nutrition_per_100g;
    if (nutr.fat_g != null) attributes["Fat (per 100g)"] = `${nutr.fat_g}g`;
    if (nutr.saturated_fat_g != null) attributes["Saturated Fat (per 100g)"] = `${nutr.saturated_fat_g}g`;
    if (nutr.sugars_g != null) attributes["Sugars (per 100g)"] = `${nutr.sugars_g}g`;
    if (nutr.sodium_mg != null) attributes["Sodium (per 100g)"] = `${nutr.sodium_mg}mg`;
  }

  // Build signals from semantic ingredients and nutrition
  const signals = [];

  // Ingredients signal
  if (semantic_ingredients?.canonical_ingredients?.length > 0) {
    signals.push({
      key: "Main Ingredients",
      value: semantic_ingredients.canonical_ingredients.slice(0, 5).join(", ")
    });
  }

  // Additives signal
  if (semantic_ingredients?.additives?.length > 0) {
    signals.push({
      key: "Additives Detected",
      value: semantic_ingredients.additives.join(", ")
    });
  }

  // Allergens signal
  if (semantic_ingredients?.allergens?.length > 0) {
    signals.push({
      key: "Allergens",
      value: semantic_ingredients.allergens.join(", ")
    });
  }

  // Health penalty signals
  if (health?.penalties) {
    const penaltyItems = Object.entries(health.penalties)
      .filter(([_, val]) => val > 0)
      .map(([key, _]) => key.replace('_', ' ').toUpperCase());
    
    if (penaltyItems.length > 0) {
      signals.push({
        key: "Health Concerns",
        value: penaltyItems.join(", ")
      });
    }
  }

  // Confidence signal
  signals.push({
    key: "Analysis Confidence",
    value: `${confidence}%`
  });

  return {
    category,
    confidence,
    labels,
    attributes,
    signals,
    // Include raw data for advanced views
    rawData: {
      health,
      semantic_ingredients,
      nutrition_normalized,
      explanation
    }
  };
}
