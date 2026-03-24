from typing import Iterable, Set, List

# Common allergens
ALLERGENS = {
    "milk": ["milk", "cream", "butter", "cheese", "yogurt", "lactose", "casein", "whey"],
    "eggs": ["egg", "eggs", "mayonnaise"],
    "peanuts": ["peanut", "peanuts"],
    "tree_nuts": ["almond", "walnut", "cashew", "pecan", "macadamia", "pistachio", "brazil nut"],
    "fish": ["fish", "salmon", "tuna", "cod", "anchovy"],
    "shellfish": ["shrimp", "crab", "lobster", "oyster", "clam", "mussel"],
    "soy": ["soy", "soybean", "tofu", "edamame"],
    "wheat": ["wheat", "barley", "rye", "gluten"],
    "sesame": ["sesame"],
}

# Common additives
ADDITIVES = {
    "artificial_colors": ["red 40", "yellow 5", "blue 1", "fd&c", "food coloring", "artificial color"],
    "preservatives": ["benzoate", "sulfite", "sorbate", "nitrate", "nitrite", "bha", "bht"],
    "artificial_sweeteners": ["sucralose", "aspartame", "acesulfame", "saccharin", "artificial sweetener"],
    "flavor_enhancers": ["monosodium glutamate", "msg"],
    "thickeners": ["xanthan gum", "carrageenan", "guar gum", "locust bean gum"],
}

# Processing indicators
PROCESSING_INDICATORS = {
    "refined": ["refined flour", "refined grain", "enriched flour", "white bread"],
    "fried": ["fried", "deep-fried"],
    "hydrogenated": ["hydrogenated", "partially hydrogenated"],
    "high_sodium": ["salt", "sodium"],
    "high_sugar": ["sugar", "corn syrup", "fructose", "dextrose", "maltodextrin", "honey", "maple syrup"],
    "artificial": ["artificial flavor", "artificial ingredient"],
}

# Ingredient tags for scoring
TAG_RULES = {
    "high_sugar": ["sugar", "corn syrup", "fructose", "dextrose", "maltodextrin"],
    "artificial_sweeteners": ["sucralose", "aspartame", "acesulfame", "saccharin"],
    "trans_fat": ["hydrogenated", "partially hydrogenated"],
    "saturated_fat": ["palm oil", "coconut oil", "shortening"],
    "refined_grains": ["enriched flour", "wheat flour", "refined", "corn flour", "rice flour"],
    "refined_starch": ["corn starch", "modified starch", "maltodextrin", "dextrose"],
    "seed_oils": ["canola oil", "soybean oil", "sunflower oil", "safflower oil", "corn oil", "vegetable oil"],
    "msg": ["monosodium glutamate", "msg"],
    "high_sodium": ["salt", "sodium"],
    "artificial_colors": ["red 40", "yellow 5", "yellow 6", "blue 1", "fd&c", "artificial color"],
    "artificial_flavors": ["artificial flavor"],
    "ultra_processed": [
        "maltodextrin",
        "monosodium glutamate",
        "artificial flavor",
        "artificial color",
        "modified starch",
        "corn syrup",
    ],
}


def tag_ingredients(ingredients: Iterable[str]) -> Set[str]:
    """Generate tags from ingredients for health scoring."""
    tags: Set[str] = set()
    for ing in ingredients:
        low = ing.lower()
        for tag, keywords in TAG_RULES.items():
            if any(k in low for k in keywords):
                tags.add(tag)
    return tags


def detect_allergens(ingredients: Iterable[str]) -> List[str]:
    """Detect common allergens in ingredients."""
    found_allergens = set()
    for ing in ingredients:
        low = ing.lower()
        for allergen_name, keywords in ALLERGENS.items():
            if any(k in low for k in keywords):
                found_allergens.add(allergen_name)
    return sorted(list(found_allergens))


def detect_additives(ingredients: Iterable[str]) -> List[str]:
    """Detect common food additives in ingredients."""
    found_additives = set()
    for ing in ingredients:
        low = ing.lower()
        for additive_name, keywords in ADDITIVES.items():
            if any(k in low for k in keywords):
                found_additives.add(additive_name)
    return sorted(list(found_additives))


def detect_processing_indicators(ingredients: Iterable[str]) -> List[str]:
    """Detect processing indicators in ingredients."""
    found_indicators = set()
    for ing in ingredients:
        low = ing.lower()
        for indicator_name, keywords in PROCESSING_INDICATORS.items():
            if any(k in low for k in keywords):
                found_indicators.add(indicator_name)
    return sorted(list(found_indicators))
