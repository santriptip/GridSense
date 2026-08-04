import pandas as pd
import matplotlib.pyplot as plt


# Load simulation data
df = pd.read_csv("energy_results.csv")


# 1. Load vs Solar
plt.figure(figsize=(10, 5))

plt.plot(
    df["hour"],
    df["load"],
    label="House Load"
)

plt.plot(
    df["hour"],
    df["solar"],
    label="Solar Generation"
)

plt.xlabel("Hour")
plt.ylabel("Power (W)")
plt.title("House Demand vs Solar Generation")

plt.legend()
plt.grid()

plt.savefig("load_vs_solar.png")


# 2. Battery State of Charge
plt.figure(figsize=(10, 5))

plt.plot(
    df["hour"],
    df["battery_soc"]
)

plt.xlabel("Hour")
plt.ylabel("Battery SoC (%)")
plt.title("Battery State of Charge")

plt.grid()

plt.savefig("battery_soc.png")


# 3. Grid Usage
plt.figure(figsize=(10, 5))

plt.bar(
    df["hour"],
    df["grid"]
)

plt.xlabel("Hour")
plt.ylabel("Grid Power (W)")
plt.title("Grid Dependence")

plt.grid()

plt.savefig("grid_usage.png")