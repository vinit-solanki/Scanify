#!/usr/bin/env python
"""
Simple test script to verify the backend works correctly.
Run this before deploying to catch configuration issues.
"""

import asyncio
import json
from pipeline import analyze_text


def test_text_analysis():
    """Test text-based analysis."""
    print("\n" + "="*60)
    print("TEST 1: Text Analysis")
    print("="*60)
    
    test_label = """
    NUTRITION FACTS
    Serving Size: 100g
    
    Calories: 250
    Total Fat: 8g
    Saturated Fat: 3g
    Trans Fat: 0g
    Cholesterol: 0mg
    Sodium: 320mg
    Total Carbohydrate: 42g
    Dietary Fiber: 3g
    Sugars: 12g
    Protein: 5g
    
    INGREDIENTS: Wheat Flour, Sugar, Palm Oil, Corn Syrup, Salt, Artificial Flavor
    """
    
    # Test weight_loss mode
    print("\nAnalyzing in 'weight_loss' mode...")
    result_wl = analyze_text(test_label, mode="weight_loss")
    print(f"Is Valid: {result_wl.get('is_valid')}")
    print(f"Health Score: {result_wl.get('health', {}).get('health_score')}")
    print(f"Health Category: {result_wl.get('health', {}).get('health_category')}")
    print(f"Confidence: {result_wl.get('overall_confidence')}")
    print(f"\nRecommendations:")
    for rec in result_wl.get('health', {}).get('recommendations', []):
        print(f"  - {rec}")
    print(f"\nExplanation: {result_wl.get('explanation', '')[:200]}...")
    
    # Test diabetes mode
    print("\n" + "-"*60)
    print("Analyzing in 'diabetes' mode...")
    result_db = analyze_text(test_label, mode="diabetes")
    print(f"Is Valid: {result_db.get('is_valid')}")
    print(f"Health Score: {result_db.get('health', {}).get('health_score')}")
    print(f"Health Category: {result_db.get('health', {}).get('health_category')}")
    
    # Test semantic ingredient analysis
    print("\n" + "-"*60)
    print("Ingredient Analysis:")
    sem_ing = result_wl.get('semantic_ingredients', {})
    print(f"  Raw Ingredients: {sem_ing.get('raw_ingredients', [])[:3]}")
    print(f"  Allergens: {sem_ing.get('allergens', [])}")
    print(f"  Additives: {sem_ing.get('additives', [])}")
    print(f"  Processing: {sem_ing.get('processing_indicators', [])}")
    
    # Test nutrition parsing
    print("\n" + "-"*60)
    print("Nutrition Analysis (per 100g):")
    nutr = result_wl.get('nutrition_normalized', {}).get('nutrition_per_100g', {})
    if nutr:
        for key in ['calories', 'protein_g', 'sugars_g', 'dietary_fiber_g']:
            print(f"  {key}: {nutr.get(key)}")
    else:
        print("  No nutrition data")
    
    return result_wl.get('is_valid', False)


def test_empty_input():
    """Test error handling."""
    print("\n" + "="*60)
    print("TEST 2: Error Handling")
    print("="*60)
    
    print("\nTesting empty input...")
    result = analyze_text("")
    print(f"Is Valid: {result.get('is_valid')}")
    print(f"Error Message: {result.get('error_message')}")
    
    return not result.get('is_valid', True)


def test_partial_data():
    """Test with incomplete nutrition data."""
    print("\n" + "="*60)
    print("TEST 3: Partial Data Handling")
    print("="*60)
    
    minimal_label = """
    NUTRITION FACTS
    Calories: 150
    Protein: 10g
    
    INGREDIENTS: Water, Salt
    """
    
    print("\nAnalyzing minimal label...")
    result = analyze_text(minimal_label)
    print(f"Is Valid: {result.get('is_valid')}")
    print(f"Health Score: {result.get('health', {}).get('health_score')}")
    print(f"Confidence: {result.get('overall_confidence')}")
    print(f"Extracted Nutrients: {len(result.get('nutrition_normalized', {}).get('nutrition_per_100g', {}))}")
    
    return result.get('is_valid', False)


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("SCANIFY BACKEND - VERIFICATION TEST")
    print("="*60)
    
    try:
        test1_pass = test_text_analysis()
        test2_pass = test_empty_input()
        test3_pass = test_partial_data()
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"✓ Text Analysis: {'PASS' if test1_pass else 'FAIL'}")
        print(f"✓ Error Handling: {'PASS' if test2_pass else 'FAIL'}")
        print(f"✓ Partial Data: {'PASS' if test3_pass else 'FAIL'}")
        
        all_pass = test1_pass and test2_pass and test3_pass
        print(f"\nOverall: {'✓ ALL TESTS PASSED' if all_pass else '✗ SOME TESTS FAILED'}")
        print("="*60 + "\n")
        
        return 0 if all_pass else 1
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
