from src.config import SimulationConfig
from src.optimizer import optimize_system, best_configuration
import random

weather_profile = [
    random.uniform(0.3, 1.0)
    for _ in range(365)
]

def main():

    # Base simulation configuration
    config = SimulationConfig(
        solar_capacity_kw=5,
        weather_factor=1.0,
        battery_capacity_kwh=10,
        initial_soc=0.5,
        peak_price=0.4,
        off_peak_price=0.2,
        solar_cost_per_kw=1000,
        battery_cost_per_kwh=500,
    )


    # Search ranges
    solar_options = [2, 4, 6, 8, 10]

    battery_options = [0, 5, 10, 15, 20]


    # Run optimization
    results = optimize_system(
        base_config=config,
        solar_options=solar_options,
        battery_options=battery_options,
        weather_profile=weather_profile,
        lifetime_years=20
    )


    # Display all configurations tested
    print("\nOptimization Results:")
    print(results.to_string(index=False))


    # Find cheapest lifetime solution
    best = best_configuration(
        results,
        objective="total_lifetime_cost"
    )


    print("\nBest Configuration:")
    print(best)


    # Save results for analysis/plotting
    results.to_csv(
        "optimization_results.csv",
        index=False
    )


if __name__ == "__main__":
    main()