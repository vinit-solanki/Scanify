import re
from typing import Dict, List, Tuple, Optional

SECTION_BREAKS = [
    "nutrition facts",
    "supplement facts",
    "allergens",
    "allergen information",
]


def _clean(text: str) -> str:
    return re.sub(r"[\t\r]", " ", text).strip()


def parse_ingredients(text: str) -> List[str]:
    """Extract a simple list of ingredients from OCR text.
    Strategy: find 'ingredients' section and split by commas; strip noise.
    """
    if not text:
        return []
    lower = text.lower()
    match = re.search(r"ingredients\s*[:\-]?\s*(.+)", lower, re.DOTALL)
    if not match:
        return []
    tail = match.group(1)
    # Stop at next section or double newline
    for br in SECTION_BREAKS:
        idx = tail.find(br)
        if idx != -1:
            tail = tail[:idx]
    tail = tail.split("\n\n")[0]
    # Remove parentheses and extra spaces
    tail = re.sub(r"[()\[\]]", " ", tail)
    # Split and clean
    parts = [p.strip() for p in tail.split(",")]
    # Remove empty and trivial tokens
    ingredients = []
    for p in parts:
        p = re.sub(r"\s+", " ", p)
        p = re.sub(r"^contains\s+", "", p)
        if p and not p.isdigit() and len(p) > 2:
            ingredients.append(p)
    return ingredients


NUTRIENT_MAP = {
    "calories": ["calories", "kcal", "energy"],
    "total_fat_g": ["total fat", "fat", "total lipid"],
    "saturated_fat_g": ["saturated fat", "sat. fat", "saturated"],
    "trans_fat_g": ["trans fat", "trans"],
    "cholesterol_mg": ["cholesterol"],
    "sodium_mg": ["sodium"],
    "carbohydrate_g": ["total carbohydrate", "carbohydrate", "carbs", "carbohydrates"],
    "dietary_fiber_g": ["dietary fiber", "fiber", "fibre"],
    "sugars_g": ["total sugars", "sugars", "sugar"],
    "protein_g": ["protein"],
}

UNIT_MULTIPLIERS = {
    "g": 1.0,
    "mg": 0.001,  # mg -> grams for most nutrients
    "kcal": 1.0,
    "cal": 1.0,
}


def _extract_value(line: str) -> Tuple[float, str]:
    """Extract numeric value and unit from a string."""
    m = re.search(r"(\d[\d,]*(?:\.\d+)?)\s*([a-zA-Z%]+)?", line)
    if not m:
        return 0.0, ""
    raw = m.group(1).replace(",", "")
    val = float(raw)
    unit = (m.group(2) or "").lower()
    return val, unit


def _is_end_of_nutrition_block(line: str) -> bool:
    """Heuristic section boundaries to avoid parsing daily-value reference tables."""
    line_l = line.lower().strip()
    if not line_l:
        return False
    return (
        line_l.startswith("ingredients")
        or line_l.startswith("contains")
        or "percent daily values" in line_l
        or "daily values are based" in line_l
        or line_l.startswith("calories per gram")
    )


def _line_matches_alias(line: str, alias: str) -> bool:
    """Check whether a nutrient alias appears in a line as a standalone phrase."""
    line_norm = f" {line.lower()} "
    alias_norm = alias.lower().strip()
    pattern = r"\b" + re.escape(alias_norm) + r"\b"
    return re.search(pattern, line_norm) is not None


def _parse_serving_size(text: str) -> Optional[Tuple[float, str]]:
    """Parse serving size from text. Returns (grams, description) or None."""
    m_serv = re.search(r"serving\s*size\s*[:\-]?\s*([^\n]+)", text, re.IGNORECASE)
    if not m_serv:
        return None

    serving_str = m_serv.group(1).strip()

    # Prefer explicit gram/ml value when present anywhere in the serving phrase
    m_g_ml = re.search(
        r"(\d+(?:\.\d+)?)\s*(g|gram|grams|ml|milliliter|milliliters)\b",
        serving_str,
        re.IGNORECASE,
    )
    if m_g_ml:
        val = float(m_g_ml.group(1))
        unit = m_g_ml.group(2).lower()
        if unit in ("g", "gram", "grams"):
            return (val, serving_str)
        # For beverages and many liquid labels, use 1ml ~= 1g
        return (val, serving_str)

    # Fall back to ounce conversion if grams are not explicitly available
    m_oz = re.search(r"(\d+(?:\.\d+)?)\s*(oz|ounce|ounces)\b", serving_str, re.IGNORECASE)
    if m_oz:
        val_oz = float(m_oz.group(1))
        return (val_oz * 28.3495, serving_str)

    # Generic fallback for edge cases where unit appears without spacing
    m = re.search(r"(\d+(?:\.\d+)?)\s*([a-z]+)", serving_str, re.IGNORECASE)
    if m:
        val = float(m.group(1))
        unit = m.group(2).lower()
        if unit in ("g", "gram", "grams", "ml", "milliliter", "milliliters"):
            return (val, serving_str)
    return None


def parse_nutrition(text: str) -> Dict[str, float]:
    """Parse nutrition facts from OCR text into a dict.
    Values are normalized to grams for nutrients; sodium stays in mg.
    Returns dict with serving_size_g and individual nutrients.
    """
    res: Dict[str, float] = {}
    if not text:
        return res
    lower = text.lower()
    
    # Extract serving size
    serving_info = _parse_serving_size(text)
    if serving_info:
        serving_g, serving_desc = serving_info
        res["serving_size_g"] = serving_g
        res["serving_size_description"] = serving_desc
    
    # Line-by-line scan for nutrients
    for line in lower.splitlines():
        line = _clean(line)
        if not line:
            continue

        # Stop once we leave the main nutrition facts block.
        if _is_end_of_nutrition_block(line):
            break

        for key, aliases in NUTRIENT_MAP.items():
            # Keep the first plausible hit for each nutrient to avoid
            # overwriting with daily-value reference rows later in text.
            if key in res:
                continue

            if any(_line_matches_alias(line, alias) for alias in aliases):
                # Avoid mapping saturated/trans fat lines to total fat when alias is generic 'fat'.
                if key == "total_fat_g" and ("saturated fat" in line or "trans fat" in line):
                    continue

                val, unit = _extract_value(line)
                if val == 0.0:
                    continue
                
                # Special handling for sodium (keep in mg)
                if key == "sodium_mg":
                    if unit == "g":
                        res[key] = val * 1000.0
                    elif unit == "mg":
                        res[key] = val
                    else:
                        res[key] = val
                else:
                    # For other nutrients, normalize to grams
                    if unit == "g":
                        res[key] = val
                    elif unit == "mg":
                        res[key] = val * 0.001
                    else:
                        res[key] = val
                break
    
    return res


def normalize_nutrition_to_per_100g(
    nutrition: Dict[str, float], serving_size_g: Optional[float] = None
) -> Dict[str, float]:
    """Convert per-serving nutrition to per 100g basis.
    If serving_size_g is not provided, assumes per 100g already.
    """
    if not serving_size_g or serving_size_g <= 0:
        return nutrition
    
    result = {}
    for key, val in nutrition.items():
        if key not in ("serving_size_g", "serving_size_description"):
            # Convert from per serving to per 100g
            result[key] = (val / serving_size_g) * 100
    return result
