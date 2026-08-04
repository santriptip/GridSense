import math


class SolarPanel:
    """
    Simple residential solar PV model.

    Generates hourly power output based on:
    - Panel size (kW)
    - Sunrise
    - Sunset
    - Weather factor
    """

    def __init__(
        self,
        capacity_kw=3.0,
        sunrise=6,
        sunset=18,
        weather_factor=1.0
    ):

        self.capacity_kw = capacity_kw
        self.sunrise = sunrise
        self.sunset = sunset
        self.weather_factor = weather_factor

    def get_power(self, hour):
        """
        Returns power output in Watts.
        """

        if hour < self.sunrise or hour > self.sunset:
            return 0

        daylight = self.sunset - self.sunrise

        x = (hour - self.sunrise) / daylight

        power = (
            math.sin(math.pi * x)
            * self.capacity_kw
            * 1000
            * self.weather_factor
        )

        return max(0, power)

    def print_daily_generation(self):

        print("\n========== SOLAR OUTPUT ==========\n")

        total = 0

        for hour in range(24):

            power = self.get_power(hour)

            total += power

            print(f"{hour:02d}:00   {power:7.1f} W")

        print("\nDaily Energy Produced:")

        print(f"{total/1000:.2f} Wh (hourly approximation)")