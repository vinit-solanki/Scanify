def infer_per_100g(nutrition, serving_size_g):
    """
    Converts per-serving nutrition to per-100g values.
    """

    inferred = {}

    factor = 100 / serving_size_g if serving_size_g else None

    for k, v in nutrition.items():
        if v is not None and factor:
            inferred[k] = round(v * factor, 1)
        else:
            inferred[k] = None

    return inferred
