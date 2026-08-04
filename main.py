from src.house import House
from src.solar import SolarPanel
from src.battery import Battery
from src.controller import EnergyController
from src.tariffs import Tariff
from src.metrics import EnergyMetrics

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

controller.save_results()

df = controller.get_dataframe()
metrics = EnergyMetrics(df)

print("\n===== SYSTEM PERFORMANCE =====")

print(
    f"Daily Load: {metrics.total_load_energy():.2f} kWh"
)

print(
    f"Solar Generated: {metrics.total_solar_energy():.2f} kWh"
)

print(
    f"Grid Energy: {metrics.grid_energy_used():.2f} kWh"
)

print(
    f"Solar Contribution: {metrics.solar_fraction():.1f}%"
)

print(
    f"Daily Cost: ${metrics.total_cost():.2f}"
)