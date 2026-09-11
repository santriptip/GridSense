from src.house import House
from src.solar import SolarPanel
from src.battery import Battery
from src.tariffs import Tariff
from src.controller import EnergyController
from src.config import SimulationConfig

import pandas as pd


def run_simulation(
    config: SimulationConfig,
    weather_profile=None
):
    """
    Run simulation over multiple days.

    Parameters
    ----------
    config : SimulationConfig
        System configuration.

    weather_profile : list, optional
        Solar generation factor for each day.
        Example:
        [1.0, 0.8, 0.5]

    Returns
    -------
    pandas.DataFrame
        Complete simulation results.
    """

    # Default to one day using configured weather
    if weather_profile is None:
        weather_profile = [
            config.weather_factor
        ]


    house = House()

    battery = Battery(
        capacity_kwh=config.battery_capacity_kwh,
        soc=config.initial_soc
    )

    tariff = Tariff(
        peak_price=config.peak_price,
        off_peak_price=config.off_peak_price
    )


    all_results = []


    for day, weather_factor in enumerate(weather_profile):

        solar = SolarPanel(
            capacity_kw=config.solar_capacity_kw,
            weather_factor=weather_factor
        )


        controller = EnergyController(
            house,
            solar,
            battery,
            tariff,
            config.peak_load_kw
        )


        controller.simulate_day(day=day + 1)

        daily_results = controller.get_dataframe()

        daily_results["day"] = day + 1

        all_results.append(
            daily_results
        )


    return pd.concat(
        all_results,
        ignore_index=True
    )