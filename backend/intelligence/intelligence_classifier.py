from ontology.ingredient_ontology import (
    INGREDIENT_SYNONYMS,
    ALLERGENS,
    SUGAR_ALIASES,
    PROCESSING_INDICATORS
)

def classify_ingredients(raw_text):
    canonical = set()
    additives = set()
    allergens = set()
    sugar_flags = set()
    processing_flags = set()

    for canonical_name, synonyms in INGREDIENT_SYNONYMS.items():
        for s in synonyms:
            if s in raw_text:
                canonical.add(canonical_name)

    for allergen, aliases in ALLERGENS.items():
        for a in aliases:
            if a in raw_text:
                allergens.add(allergen)

    for sugar in SUGAR_ALIASES:
        if sugar in raw_text:
            sugar_flags.add("added sugar")

    for proc in PROCESSING_INDICATORS:
        if proc in raw_text:
            processing_flags.add(proc)

    for add in ["phosphate", "vanillin"]:
        if add in canonical:
            additives.add(add)

    return {
        "canonical_ingredients": sorted(canonical),
        "additives": sorted(additives),
        "allergens": sorted(allergens),
        "sugar_indicators": sorted(sugar_flags),
        "processing_indicators": sorted(processing_flags)
    }
