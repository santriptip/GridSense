from src.house import House
from src.solar import SolarPanel
from src.battery import Battery
from src.tariffs import Tariff
from src.controller import EnergyController
from src.config import SimulationConfig

def run_simulation(config: SimulationConfig):

    house = House()

    solar = SolarPanel(
        capacity_kw=config.solar_capacity_kw,
        weather_factor=config.weather_factor
    )

    battery = Battery(
        capacity_kwh=config.battery_capacity_kwh,
        soc=config.initial_soc 
    )

    tariff = Tariff(
        peak_price=config.peak_price,
        off_peak_price=config.off_peak_price
    )

    controller = EnergyController(
        house,
        solar,
        battery,
        tariff
    )

    controller.simulate_day()

    return controller.get_dataframe()