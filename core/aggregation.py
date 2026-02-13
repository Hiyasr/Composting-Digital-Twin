def parse_range(value):
    if value is None or value == "–":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str) and "–" in value:
        low, high = value.split("–")
        return (float(low) + float(high)) / 2
    return None


def weighted_average(old_val, old_mass, new_val, new_mass):
    return ((old_val * old_mass) + (new_val * new_mass)) / (old_mass + new_mass)


def add_waste(state, waste_props, waste_mass):
    """
    Mix new waste into the compost bin
    """

    # 🚫 Block non-compostable items
    timeframe = str(waste_props.get("Timeframe", "")).lower()
    if "cannot" in timeframe or "indefinite" in timeframe:
        raise ValueError("Item contains synthetics/biohazards and is Non-Processable.")
    
    temp = parse_range(waste_props.get("Target Temp (°C)"))
    moisture = parse_range(waste_props.get("Moisture (%)"))
    ph = parse_range(waste_props.get("Optimal pH"))

    if temp is not None:
        state.temperature = weighted_average(
            state.temperature, state.mass, temp, waste_mass
        )

    if moisture is not None:
        state.moisture = weighted_average(
            state.moisture, state.mass, moisture, waste_mass
        )

    if ph is not None:
        state.pH = weighted_average(
            state.pH, state.mass, ph, waste_mass
        )

    state.mass += waste_mass
    return state
