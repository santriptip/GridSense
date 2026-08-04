import streamlit as st
import matplotlib.pyplot as plt

from src.house import House
from src.solar import SolarPanel
from src.battery import Battery
from src.tariffs import Tariff
from src.controller import EnergyController
from src.metrics import EnergyMetrics


# ----------------------------
# Page setup
# ----------------------------

st.set_page_config(
    page_title="GridSense",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ GridSense Energy Dashboard")

st.write(
    "Residential microgrid simulation platform "
    "for solar generation, battery storage, and electricity tariffs."
)


# ----------------------------
# Sidebar controls
# ----------------------------

st.sidebar.header("Simulation Settings")


solar_capacity = st.sidebar.slider(
    "Solar Capacity (kW)",
    min_value=1.0,
    max_value=10.0,
    value=3.0,
    step=0.5
)


battery_capacity = st.sidebar.slider(
    "Battery Capacity (kWh)",
    min_value=1.0,
    max_value=30.0,
    value=10.0,
    step=1.0
)


weather_factor = st.sidebar.slider(
    "Weather Factor",
    min_value=0.3,
    max_value=1.0,
    value=0.9,
    step=0.05
)


initial_soc = st.sidebar.slider(
    "Initial Battery Charge (%)",
    min_value=0,
    max_value=100,
    value=50,
    step=5
)


peak_price = st.sidebar.slider(
    "Peak Electricity Price ($/kWh)",
    min_value=0.1,
    max_value=1.0,
    value=0.4,
    step=0.05
)


off_peak_price = st.sidebar.slider(
    "Off-Peak Electricity Price ($/kWh)",
    min_value=0.05,
    max_value=0.5,
    value=0.2,
    step=0.05
)


# ----------------------------
# Run simulation
# ----------------------------

house = House()


solar = SolarPanel(
    capacity_kw=solar_capacity,
    weather_factor=weather_factor
)


battery = Battery(
    capacity_kwh=battery_capacity,
    soc=initial_soc / 100
)


tariff = Tariff(
    peak_price=peak_price,
    off_peak_price=off_peak_price
)


controller = EnergyController(
    house,
    solar,
    battery,
    tariff
)


controller.simulate_day()


df = controller.get_dataframe()


# ----------------------------
# Metrics
# ----------------------------

metrics = EnergyMetrics(df)


st.header("System Performance")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Daily Consumption",
        f"{metrics.total_load_energy():.2f} kWh"
    )


with col2:
    st.metric(
        "Solar Generated",
        f"{metrics.total_solar_energy():.2f} kWh"
    )


with col3:
    st.metric(
        "Grid Energy",
        f"{metrics.grid_energy_used():.2f} kWh"
    )


with col4:
    st.metric(
        "Daily Cost",
        f"${metrics.total_cost():.2f}"
    )


# ----------------------------
# Load vs Solar Plot
# ----------------------------

st.header("Power Generation Profile")


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
ax.set_title("Load vs Solar Generation")

ax.legend()
ax.grid()


st.pyplot(fig)


# ----------------------------
# Battery Plot
# ----------------------------

st.header("Battery State of Charge")


fig, ax = plt.subplots(figsize=(10, 4))


ax.plot(
    df["hour"],
    df["battery_soc"]
)


ax.set_xlabel("Hour")
ax.set_ylabel("SoC (%)")
ax.set_title("Battery Charging Profile")

ax.grid()


st.pyplot(fig)


# ----------------------------
# Grid Usage Plot
# ----------------------------

st.header("Grid Dependency")


fig, ax = plt.subplots(figsize=(10, 4))


ax.bar(
    df["hour"],
    df["grid"]
)


ax.set_xlabel("Hour")
ax.set_ylabel("Grid Power (W)")
ax.set_title("Grid Import")


ax.grid()


st.pyplot(fig)


# ----------------------------
# Raw Data
# ----------------------------

with st.expander("View Simulation Data"):

    st.dataframe(df)