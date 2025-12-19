def estimate_calories(fat_g, carbs_g, protein_g):
    if fat_g is None or carbs_g is None or protein_g is None:
        return None
    return round(fat_g * 9 + carbs_g * 4 + protein_g * 4)


def midpoint(low, high):
    return round((low + high) / 2, 1)
