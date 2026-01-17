#!/usr/bin/env python
"""
Integration test script to verify the backend works with frontend expectations.
This script tests the actual HTTP API endpoints.

Usage:
    python test_api.py              # Tests against http://localhost:5000
    python test_api.py http://example.com:5000   # Custom URL
"""

import asyncio
import json
import sys
import httpx
from pathlib import Path


BASE_URL = "http://localhost:5000"


async def test_health_endpoint():
    """Test health check endpoint."""
    print("\n" + "="*60)
    print("TEST: Health Check")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False


async def test_modes_endpoint():
    """Test modes endpoint."""
    print("\n" + "="*60)
    print("TEST: Available Modes")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/modes")
            print(f"Status: {response.status_code}")
            modes = response.json()
            print(f"Available modes: {len(modes.get('modes', []))}")
            for mode in modes.get('modes', []):
                print(f"  - {mode['id']}: {mode['name']}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False


async def test_text_analysis():
    """Test text-based analysis endpoint."""
    print("\n" + "="*60)
    print("TEST: Text Analysis")
    print("="*60)
    
    label_text = """
    NUTRITION FACTS
    Serving Size: 100g
    
    Calories: 250
    Total Fat: 8g
    Saturated Fat: 3g
    Sodium: 320mg
    Total Carbohydrate: 42g
    Dietary Fiber: 3g
    Sugars: 12g
    Protein: 5g
    
    INGREDIENTS: Wheat Flour, Sugar, Palm Oil, Salt
    """
    
    payload = {
        "label_text": label_text,
        "mode": "weight_loss"
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(
                f"{BASE_URL}/analyze",
                json=payload
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✓ Response received")
                print(f"  - is_valid: {data.get('is_valid')}")
                print(f"  - health_score: {data.get('health', {}).get('health_score')}")
                print(f"  - health_category: {data.get('health', {}).get('health_category')}")
                print(f"  - confidence: {data.get('overall_confidence')}")
                
                # Check for required fields
                required_fields = [
                    'is_valid', 'mode', 'semantic_ingredients',
                    'nutrition_normalized', 'health', 'overall_confidence'
                ]
                missing = [f for f in required_fields if f not in data]
                if missing:
                    print(f"❌ Missing fields: {missing}")
                    return False
                
                print(f"✓ All required fields present")
                return True
            else:
                print(f"Error: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False


async def test_invalid_input():
    """Test error handling."""
    print("\n" + "="*60)
    print("TEST: Error Handling")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        try:
            # Test empty label
            response = await client.post(
                f"{BASE_URL}/analyze",
                json={"label_text": "", "mode": "weight_loss"}
            )
            print(f"Empty label - Status: {response.status_code}")
            
            if response.status_code == 400:
                print(f"✓ Correctly rejected empty input")
                return True
            else:
                print(f"✗ Expected 400, got {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False


async def test_modes_functionality():
    """Test different analysis modes."""
    print("\n" + "="*60)
    print("TEST: Analysis Modes")
    print("="*60)
    
    label_text = """
    NUTRITION FACTS
    Serving Size: 100g
    Calories: 300
    Sugars: 18g
    Protein: 4g
    Fiber: 2g
    """
    
    modes = ["general", "weight_loss", "diabetes"]
    results = {}
    
    async with httpx.AsyncClient(timeout=30) as client:
        for mode in modes:
            try:
                response = await client.post(
                    f"{BASE_URL}/analyze",
                    json={"label_text": label_text, "mode": mode}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    score = data.get('health', {}).get('health_score')
                    results[mode] = score
                    print(f"  {mode:15} → Score: {score}")
                else:
                    print(f"  {mode:15} → Error: {response.status_code}")
                    return False
            except Exception as e:
                print(f"  {mode:15} → Exception: {str(e)}")
                return False
    
    print(f"\n✓ All modes working (different scores expected)")
    return True


async def main():
    """Run all API tests."""
    if len(sys.argv) > 1:
        global BASE_URL
        BASE_URL = sys.argv[1]
    
    print("\n" + "="*60)
    print("SCANIFY BACKEND - API INTEGRATION TEST")
    print(f"Server: {BASE_URL}")
    print("="*60)
    
    try:
        # Run tests
        tests = [
            ("Health Check", test_health_endpoint),
            ("Modes Endpoint", test_modes_endpoint),
            ("Text Analysis", test_text_analysis),
            ("Error Handling", test_invalid_input),
            ("Mode Functionality", test_modes_functionality),
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                result = await test_func()
                results[test_name] = result
            except Exception as e:
                print(f"❌ Exception in {test_name}: {str(e)}")
                results[test_name] = False
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        for test_name, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{status:8} {test_name}")
        
        all_passed = all(results.values())
        print("\n" + ("="*60))
        if all_passed:
            print("✓ ALL TESTS PASSED - Backend is ready!")
        else:
            print("✗ Some tests failed - Check configuration")
        print("="*60 + "\n")
        
        return 0 if all_passed else 1
    
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
