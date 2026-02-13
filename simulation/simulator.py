from copy import deepcopy
import math


# -------------------------------------------------
# ENVIRONMENT + BIO MODEL
# -------------------------------------------------

def temperature_factor(temp):
    """
    Microbes grow best around 55°C (thermophilic phase)
    Gaussian response curve
    """
    optimal = 55
    sigma = 15
    return math.exp(-((temp - optimal) ** 2) / (2 * sigma ** 2))


def moisture_factor(moisture):
    """
    Ideal compost moisture ≈ 0.6
    """
    optimal = 0.6
    sigma = 0.2
    return math.exp(-((moisture - optimal) ** 2) / (2 * sigma ** 2))


def compute_microbial_activity(state):
    """
    Formula: Microbial Activity = (Temp Score * Moisture Score * pH Score) * Oxygen Level [cite: 51]
    """
    # Ideal zones from your documentation [cite: 35, 38, 42]
    temp_score = 1.0 if 45 <= state["temperature"] <= 65 else 0.2
    moist_score = 1.0 if 50 <= state["moisture"] <= 65 else 0.2
    ph_score = 1.0 if 6.5 <= state["pH"] <= 8.0 else 0.2
    
    # If any single factor is bad, the whole activity drops [cite: 52]
    activity = (temp_score * moist_score * ph_score) * state.get("oxygen", 1.0)
    return max(0.0, min(activity, 1.0))


def degradation_rate(activity):
    """
    First-order decay model
    Higher microbial activity → faster decomposition
    """
    k = 0.04  # base degradation constant
    return k * activity


# -------------------------------------------------
# SINGLE DAY SIMULATION STEP
# -------------------------------------------------

def simulate_day(state):
    """
    Updates compost state for one day
    """

    # --- calculate microbial activity ---
    activity = compute_microbial_activity(state)
    state["microbial_activity"] = activity

    # --- degradation equation ---
    rate = degradation_rate(activity)
    mass_loss = state["mass"] * rate
    state["mass"] -= mass_loss

    # --- temperature dynamics ---
    # microbes generate heat when active
    state["temperature"] += activity * 3 - 1.2

    # clamp realistic range
    state["temperature"] = max(20, min(70, state["temperature"]))

    # --- moisture evaporation ---
    state["moisture"] -= 0.002 + activity * 0.003
    state["moisture"] = max(0.3, min(0.8, state["moisture"]))

    # --- pH drift ---
    state["pH"] += (activity - 0.5) * 0.05
    state["pH"] = max(5.5, min(8.5, state["pH"]))

    # --- next day ---
    state["day"] += 1


# -------------------------------------------------
# MAIN SIMULATION LOOP
# -------------------------------------------------

def run_simulation(bin_state, days=60):
    """
    Runs compost simulation for N days
    Accepts a BinState object or dict and returns history for dashboard graphs
    """
    # Handle both dict and BinState object
    if isinstance(bin_state, dict):
        current_mass = float(bin_state['mass'])
        temp = bin_state['temperature']
        moist = bin_state['moisture']
        ph = bin_state['pH']
        oxy = bin_state['oxygen']
        micro = bin_state['microbial_activity']
    else:
        current_mass = float(bin_state.mass)
        temp = bin_state.temperature
        moist = bin_state.moisture
        ph = bin_state.pH
        oxy = bin_state.oxygen
        micro = bin_state.microbial_activity
    
    state = {
        "day": 0,
        "mass": current_mass,
        "initial_mass": current_mass,
        "temperature": temp,
        "moisture": moist,
        "pH": ph,
        "oxygen": oxy,
        "microbial_activity": micro
    }

    history = []

    for _ in range(days):
        simulate_day(state)

        history.append({
            "day": state["day"],
            "mass": state["mass"],
            "temperature": state["temperature"],
            "moisture": state["moisture"],
            "pH": state["pH"],
            "microbial_activity": state["microbial_activity"]
        })

    return history