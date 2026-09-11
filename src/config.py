@dataclass
class SimulationConfig:

    # Solar parameters
    solar_capacity_kw: float
    weather_factor: float = 1.0

    # Load parameters
    peak_load_kw: float = 3.0

    # Battery parameters
    battery_capacity_kwh: float = 10
    initial_soc: float = 0.5

    # Tariff parameters
    peak_price: float = 0.4
    off_peak_price: float = 0.2

    # Cost assumptions
    solar_cost_per_kw: float = 1000
    battery_cost_per_kwh: float = 800


    def __post_init__(self):

        if self.solar_capacity_kw <= 0:
            raise ValueError(
                "Solar capacity must be greater than zero."
            )

        if self.peak_load_kw <= 0:
            raise ValueError(
                "Peak load must be greater than zero."
            )

        if self.battery_capacity_kwh < 0:
            raise ValueError(
                "Battery capacity cannot be negative."
            )

        if not 0 <= self.initial_soc <= 1:
            raise ValueError(
                "Initial SOC must be between 0 and 1."
            )

        if not 0 <= self.weather_factor <= 1:
            raise ValueError(
                "Weather factor must be between 0 and 1."
            )

        if self.peak_price < 0 or self.off_peak_price < 0:
            raise ValueError(
                "Electricity prices cannot be negative."
            )