from src.house import House
from src.solar import SolarPanel
from src.battery import Battery
from src.controller import EnergyController
from src.tariffs import Tariff


house = House()


solar = SolarPanel(
    capacity_kw=3,
    weather_factor=0.9
)


battery = Battery(
    capacity_kwh=10,
    soc=0.5
)


tariff = Tariff(
    peak_price=0.4,
    off_peak_price=0.20
)


controller = EnergyController(
    house,
    solar,
    battery,
    tariff
)


controller.simulate_day()

controller.print_results()