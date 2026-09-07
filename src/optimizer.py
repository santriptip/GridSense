import pandas as pd

from src.config import SimulationConfig
from src.simulation import run_simulation
from src.metrics import EnergyMetrics


def evaluate_configuration(
    config,
    weather_profile,
    lifetime_years=20
):
    """
    Evaluate a single solar + battery configuration
    over a weather profile.
    """

    df = run_simulation(
        config,
        weather_profile
    )

    metrics = EnergyMetrics(df)

    # Total energy imported from grid
    grid_usage_kwh = float(
        metrics.grid_energy_used()
    )

    # Cost of electricity purchased from grid
    total_grid_cost = float(
        metrics.total_cost()
    )

    # Convert multi-day cost to annual cost
    simulation_days = len(weather_profile)

    if simulation_days > 0:
        annual_grid_cost = (
            total_grid_cost
            / simulation_days
            * 365
        )
    else:
        annual_grid_cost = 0


    lifetime_grid_cost = (
        annual_grid_cost
        * lifetime_years
    )


    installation_cost = (
        config.solar_capacity_kw
        * config.solar_cost_per_kw
        +
        config.battery_capacity_kwh
        * config.battery_cost_per_kwh
    )


    total_lifetime_cost = (
        installation_cost
        +
        lifetime_grid_cost
    )


    return {
        "grid_usage_kwh": grid_usage_kwh,
        "annual_grid_cost": annual_grid_cost,
        "lifetime_grid_cost": lifetime_grid_cost,
        "installation_cost": installation_cost,
        "total_lifetime_cost": total_lifetime_cost,
    }



def optimize_system(
    base_config,
    solar_options,
    battery_options,
    weather_profile,
    lifetime_years=20
):
    """
    Brute-force optimization over solar and battery sizes
    using a multi-day weather profile.
    """

    results = []


    for solar_size in solar_options:

        for battery_size in battery_options:

            config = SimulationConfig(
                solar_capacity_kw=solar_size,
                weather_factor=base_config.weather_factor,
                battery_capacity_kwh=battery_size,
                initial_soc=base_config.initial_soc,
                peak_price=base_config.peak_price,
                off_peak_price=base_config.off_peak_price,
                solar_cost_per_kw=base_config.solar_cost_per_kw,
                battery_cost_per_kwh=base_config.battery_cost_per_kwh,
            )


            evaluation = evaluate_configuration(
                config,
                weather_profile,
                lifetime_years
            )


            evaluation.update(
                {
                    "solar_size_kw": solar_size,
                    "battery_size_kwh": battery_size,
                }
            )


            results.append(evaluation)


    df = pd.DataFrame(results)


    # Keep important columns first
    column_order = [
        "solar_size_kw",
        "battery_size_kwh",
        "grid_usage_kwh",
        "annual_grid_cost",
        "lifetime_grid_cost",
        "installation_cost",
        "total_lifetime_cost",
    ]

    return df[column_order]



def best_configuration(
    results,
    objective="total_lifetime_cost",
    minimize=True
):
    """
    Return best configuration based on objective.
    """

    if objective not in results.columns:
        raise ValueError(
            f"{objective} is not a valid objective."
        )


    if minimize:
        return results.loc[
            results[objective].idxmin()
        ]

    return results.loc[
        results[objective].idxmax()
    ]



def filter_constraints(
    results,
    max_budget=None,
    max_grid_usage=None
):
    """
    Filter configurations using engineering constraints.
    """

    filtered = results.copy()


    if max_budget is not None:
        filtered = filtered[
            filtered["installation_cost"]
            <= max_budget
        ]


    if max_grid_usage is not None:
        filtered = filtered[
            filtered["grid_usage_kwh"]
            <= max_grid_usage
        ]


    return filtered