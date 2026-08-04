import pandas as pd

from src.config import SimulationConfig
from src.simulation import run_simulation
from src.metrics import EnergyMetrics


def optimize_battery(
    solar_capacity_kw,
    battery_options,
    weather_factor=1.0,
    initial_soc=0.5,
    peak_price=0.4,
    off_peak_price=0.2,
    solar_cost_per_kw=1000,
    battery_cost_per_kwh=800
):

    results = []

    solar_cost = solar_capacity_kw * solar_cost_per_kw

    for battery_size in battery_options:

        config = SimulationConfig(
            solar_capacity_kw=solar_capacity_kw,
            battery_capacity_kwh=battery_size,
            weather_factor=weather_factor,
            initial_soc=initial_soc,
            peak_price=peak_price,
            off_peak_price=off_peak_price,
            solar_cost_per_kw=solar_cost_per_kw,
            battery_cost_per_kwh=battery_cost_per_kwh
        )

        df = run_simulation(config)

        metrics = EnergyMetrics(df)

        battery_cost = battery_size * battery_cost_per_kwh

        results.append(
            {
                "battery_size_kwh": battery_size,
                "daily_energy_cost": float(metrics.total_cost()),
                "grid_usage_kwh": float(metrics.grid_energy_used()),
                "system_cost": float(
                    solar_cost + battery_cost
                )
            }
        )

    return pd.DataFrame(results)