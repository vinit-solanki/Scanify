def confidence_from_range(low, high):
    span = high - low
    if span <= 10:
        return 0.75
    elif span <= 20:
        return 0.6
    else:
        return 0.5
