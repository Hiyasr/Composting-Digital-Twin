from core.scoring import compute_microbial_activity
from core.decay import apply_decay


def simulate_day(state):
    """
    Simulates one composting day
    """
    compute_microbial_activity(state)
    apply_decay(state)
    state.day += 1
    return state
