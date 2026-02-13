def apply_decay(state, decay_constant=0.02):
    mass_loss = state.microbial_activity * decay_constant * state.mass
    state.mass -= mass_loss
    return state
