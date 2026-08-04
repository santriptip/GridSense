import streamlit as st
import matplotlib.pyplot as plt

from src.simulation import run_simulation
from src.config import SimulationConfig
from src.metrics import EnergyMetrics


# ----------------------------
# Page setup
# ----------------------------

st.set_page_config(
    page_title="GridSense Energy Dashboard",
    layout="wide"
)

st.title("GridSense Energy Dashboard")

st.write(
    "Simulation and analysis platform for residential "
    "solar generation, battery storage, and grid interaction."
)


# ----------------------------
# Session state
# ----------------------------

if "df" not in st.session_state:
    st.session_state.df = None


# ----------------------------
# Sidebar controls
# ----------------------------

st.sidebar.header("System Parameters")


solar_capacity = st.sidebar.slider(
    "Solar Capacity (kW)",
    1.0,
    10.0,
    3.0,
    0.5
)


battery_capacity = st.sidebar.slider(
    "Battery Capacity (kWh)",
    1.0,
    30.0,
    10.0,
    1.0
)


weather_factor = st.sidebar.slider(
    "Weather Factor",
    0.3,
    1.0,
    0.9,
    0.05
)


initial_soc = st.sidebar.slider(
    "Initial Battery Charge (%)",
    0,
    100,
    50,
    5
)


peak_price = st.sidebar.slider(
    "Peak Electricity Price ($/kWh)",
    0.1,
    1.0,
    0.4,
    0.05
)


off_peak_price = st.sidebar.slider(
    "Off-Peak Electricity Price ($/kWh)",
    0.05,
    0.5,
    0.2,
    0.05
)


run_button = st.sidebar.button("Run Simulation")


# ----------------------------
# Run simulation
# ----------------------------

if run_button:

    config = SimulationConfig(
        solar_capacity_kw=solar_capacity,
        battery_capacity_kwh=battery_capacity,
        weather_factor=weather_factor,
        initial_soc=initial_soc / 100,
        peak_price=peak_price,
        off_peak_price=off_peak_price
    )

    st.session_state.df = run_simulation(config)


# ----------------------------
# Display results
# ----------------------------

if st.session_state.df is None:

    st.info(
        "Configure the system parameters and run the simulation."
    )

else:

    df = st.session_state.df

    metrics = EnergyMetrics(df)


    # ------------------------
    # Metrics
    # ------------------------

    st.header("Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Daily Energy Consumption",
            f"{metrics.total_load_energy():.2f} kWh"
        )

    with col2:
        st.metric(
            "Solar Generation",
            f"{metrics.total_solar_energy():.2f} kWh"
        )

    with col3:
        st.metric(
            "Grid Import",
            f"{metrics.grid_energy_used():.2f} kWh"
        )

    with col4:
        st.metric(
            "Operating Cost",
            f"${metrics.total_cost():.2f}"
        )


    # ------------------------
    # Power profile
    # ------------------------

    st.header("Power Profile")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        df["hour"],
        df["load"],
        label="House Load"
    )

    ax.plot(
        df["hour"],
        df["solar"],
        label="Solar Generation"
    )

    ax.set_xlabel("Hour")
    ax.set_ylabel("Power (W)")
    ax.set_title("House Load and Solar Generation")

    ax.legend()
    ax.grid()

    st.pyplot(fig)


    # ------------------------
    # Battery profile
    # ------------------------

    st.header("Battery State of Charge")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        df["hour"],
        df["battery_soc"]
    )

    ax.set_xlabel("Hour")
    ax.set_ylabel("State of Charge")
    ax.set_title("Battery Storage Profile")

    ax.grid()

    st.pyplot(fig)


    # ------------------------
    # Grid profile
    # ------------------------

    st.header("Grid Import Profile")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.bar(
        df["hour"],
        df["grid"]
    )

    ax.set_xlabel("Hour")
    ax.set_ylabel("Grid Power (W)")
    ax.set_title("Grid Electricity Usage")

    ax.grid()

    st.pyplot(fig)


    # ------------------------
    # Raw data
    # ------------------------

    with st.expander("Simulation Data"):
        st.dataframe(df)