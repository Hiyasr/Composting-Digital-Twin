def score_range(value, min_val, max_val):
    if value < min_val or value > max_val:
        return 0.0

    midpoint = (min_val + max_val) / 2
    return 1 - abs(value - midpoint) / (max_val - min_val)


def compute_microbial_activity(state):
    temp_score = score_range(state.temperature, 40, 65)
    moisture_score = score_range(state.moisture, 50, 60)
    pH_score = score_range(state.pH, 6.5, 8.0)

    state.microbial_activity = (
        temp_score *
        moisture_score *
        pH_score *
        state.oxygen
    )

    return state.microbial_activity
