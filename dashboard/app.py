import sys
import os
import streamlit as st
import plotly.express as px
import pandas as pd

# --- PATH INJECTION ---
# This allows the app to find 'core' and 'simulation' on the Streamlit server
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.bin_state import BinState
from core.waste_database import WasteDatabase
from core.aggregation import add_waste
from simulation.simulator import run_simulation

# App Config
st.set_page_config(page_title="AI Composting Digital Twin", layout="wide")
st.title("♻️ AI-Driven Composting Digital Twin")
st.caption("Software-first simulation of intelligent biodegradation")

# Load Waste Database
@st.cache_data
def load_database():
    # Use relative path for GitHub/Streamlit Cloud deployment 
    path = "data/raw/rectified_waste_properties.csv"
    return WasteDatabase(path)

db = load_database()

# Sidebar: User Inputs
st.sidebar.header("🧪 Waste Input Control")
waste_type = st.sidebar.selectbox("Select Waste Type", db.list_waste_types())
waste_mass = st.sidebar.slider("Waste Mass Added (kg)", 0.1, 2.0, 0.5)
simulate_days = st.sidebar.slider("Simulation Duration (days)", 5, 60, 30)
run_button = st.sidebar.button("🚀 Run Simulation")

# Initial Bin State (Step 1: Digital Intake)
if "bin_state" not in st.session_state:
    st.session_state.bin_state = BinState(
        mass=5.0,
        temperature=30.0,
        moisture=55.0,  # Goal: 50-60% saturation [cite: 42]
        pH=7.0,         # Goal: pH between 6.5 and 8.0 [cite: 35]
        oxygen=1.0,     # Essential for microbial engine [cite: 51]
        microbial_activity=0.2
    )

# Run Simulation (Input -> Process -> Act)
if run_button:
    # Step 1: Retrieve static chemical properties [cite: 21]
    waste_props = db.get_waste(waste_type)

    # Step 2: Aggregation Logic [cite: 22]
    st.session_state.bin_state = add_waste(
        st.session_state.bin_state,
        waste_props,
        waste_mass
    )

    # Step 3 & 4: The AI Brain (Simulation & Actuation) [cite: 32]
    # Simulates weeks of decomposition in seconds [cite: 14]
    history = run_simulation(
        st.session_state.bin_state,
        days=simulate_days
    )
    st.session_state.history = history

# Dashboard Output (Step 5: Visualization)
if "history" in st.session_state:
    history = st.session_state.history
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Final Mass (kg)", round(history[-1]["mass"], 2))
    with col2:
        st.metric("Final Microbial Activity", round(history[-1]["microbial_activity"], 2))
    with col3:
        # Rate of Decay = f(Microbial Activity) [cite: 47]
        efficiency = (1 - history[-1]["mass"] / history[0]["mass"]) * 100
        st.metric("Degradation Efficiency (%)", round(efficiency, 1))

    st.subheader("📉 Degradation Curve")
    st.plotly_chart(px.line(history, x="day", y="mass", title="Biomass Reduction Over Time"), use_container_width=True)
    st.plotly_chart(px.line(history, x="day", y="microbial_activity", title="Microbial Activity Index"), use_container_width=True)
else:
    st.info("👈 Add waste and run the simulation to see results.")
