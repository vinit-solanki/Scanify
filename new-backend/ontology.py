import re
from typing import Iterable, Set, List, Dict

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

# Additive code ontology (INS/E code style).
# Keys are category labels used in API output.
# Values are normalized additive code stems without prefix, optionally with suffix.
ADDITIVE_CODE_MAP: Dict[str, Set[str]] = {
    "preservatives": {
        "200", "201", "202", "203", "210", "211", "212", "213",
        "220", "221", "222", "223", "224", "226", "227", "228",
        "249", "250", "251", "252", "280", "281", "282", "283",
    },
    "artificial_colors": {
        "102", "104", "110", "120", "122", "123", "124", "127",
        "129", "132", "133", "142", "150a", "150b", "150c", "150d",
    },
    "artificial_sweeteners": {
        "950", "951", "952", "954", "955", "956", "960", "961",
    },
    "flavor_enhancers": {
        "620", "621", "622", "623", "624", "625", "627", "631", "635",
    },
    "thickeners": {
        "400", "401", "402", "403", "404", "405", "406", "407", "410",
        "412", "414", "415", "440", "466",
    },
    "emulsifiers": {
        "322", "471", "472a", "472b", "472c", "472d", "472e", "472f",
        "476", "481", "482", "491", "492", "493", "494", "495",
    },
    "acidity_regulators": {
        "296", "330", "331", "332", "333", "334", "335", "336", "337",
        "338", "339", "340", "341", "500", "500i", "500ii", "500iii",
        "501", "503", "503ii", "504", "524", "525", "526",
    },
}

# Code-driven tags that should influence health scoring similarly to keyword tags.
TAG_CODE_RULES: Dict[str, Set[str]] = {
    "artificial_colors": ADDITIVE_CODE_MAP["artificial_colors"],
    "artificial_sweeteners": ADDITIVE_CODE_MAP["artificial_sweeteners"],
    "msg": {"621"},
    "ultra_processed": (
        ADDITIVE_CODE_MAP["artificial_colors"]
        | ADDITIVE_CODE_MAP["artificial_sweeteners"]
        | ADDITIVE_CODE_MAP["flavor_enhancers"]
    ),
}


def _roman_to_ascii(roman: str) -> str:
    r = (roman or "").strip().lower().replace(" ", "")
    mapping = {
        "i": "i",
        "ii": "ii",
        "iii": "iii",
        "iv": "iv",
        "v": "v",
        "vi": "vi",
    }
    return mapping.get(r, "")


def _extract_additive_codes(text: str) -> Set[str]:
    """Extract normalized additive codes from text.

    Supports forms like:
    - INS 500(ii), INS-500(ii), INS500(ii)
    - INR 500 ii (common OCR confusion for INS)
    - E403, E 403, E-403
    - plain 500(i) when listed in additive context
    """
    low = (text or "").lower()
    if not low:
        return set()

    codes: Set[str] = set()

    prefixed_pattern = re.compile(
        r"\b(?:ins|inr|e)\s*[-:]?\s*(\d{3,4})\s*(?:[\(\[]?\s*([ivx]{1,4}|[a-f])\s*[\)\]]?)?\b"
    )
    plain_parenthesized_pattern = re.compile(r"\b(\d{3,4})\s*\(\s*([ivx]{1,4}|[a-f])\s*\)\b")
    plain_letter_suffix_pattern = re.compile(r"\b(\d{3,4})([a-f])\b")

    for m in prefixed_pattern.finditer(low):
        base = m.group(1)
        suffix_raw = m.group(2)
        suffix = _roman_to_ascii(suffix_raw) if suffix_raw and suffix_raw.isalpha() else (suffix_raw or "")
        suffix = (suffix or "").lower()
        codes.add(base)
        if suffix:
            codes.add(f"{base}{suffix}")

    for m in plain_parenthesized_pattern.finditer(low):
        base = m.group(1)
        suffix = _roman_to_ascii(m.group(2))
        codes.add(base)
        if suffix:
            codes.add(f"{base}{suffix}")

    for m in plain_letter_suffix_pattern.finditer(low):
        base = m.group(1)
        suffix = m.group(2).lower()
        codes.add(base)
        codes.add(f"{base}{suffix}")

    return codes


def _codes_hit_category(codes: Set[str], category_codes: Set[str]) -> bool:
    for c in codes:
        if c in category_codes:
            return True
        # Also allow base-code matching when detected code has suffix.
        base = re.match(r"^(\d{3,4})", c)
        if base and base.group(1) in category_codes:
            return True
    return False

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

        additive_codes = _extract_additive_codes(low)
        if additive_codes:
            for tag, category_codes in TAG_CODE_RULES.items():
                if _codes_hit_category(additive_codes, category_codes):
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

        additive_codes = _extract_additive_codes(low)
        if additive_codes:
            for additive_name, category_codes in ADDITIVE_CODE_MAP.items():
                if _codes_hit_category(additive_codes, category_codes):
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

        additive_codes = _extract_additive_codes(low)
        if additive_codes:
            found_indicators.add("additive_codes")

            if _codes_hit_category(additive_codes, ADDITIVE_CODE_MAP["preservatives"]):
                found_indicators.add("preservative_codes")

            if _codes_hit_category(additive_codes, ADDITIVE_CODE_MAP["artificial_colors"]):
                found_indicators.add("artificial_color_codes")
    return sorted(list(found_indicators))
