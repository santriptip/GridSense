import pandas as pd


class EnergyController:

    def __init__(self, house, solar, battery, tariff):

        self.house = house
        self.solar = solar
        self.battery = battery
        self.tariff = tariff

        self.results = []
        self.total_cost = 0


    def simulate_day(self, day=1, reset=False):

        """
        Simulate one day of operation.

        Parameters
        ----------
        day : int
            Simulation day number.

        reset : bool
            Clears previous results if starting a new simulation.
        """

        if reset:
            self.results = []
            self.total_cost = 0


        for hour in range(24):

            load = self.house.get_total_load(hour)

            solar_power = self.solar.get_power(hour)

            net_power = solar_power - load

            grid_power = 0


            # Excess solar
            if net_power > 0:

                self.battery.charge(net_power)


            # Solar deficit
            else:

                deficit = abs(net_power)

                battery_power = self.battery.discharge(
                    deficit
                )

                remaining_deficit = (
                    deficit - battery_power
                )


                if remaining_deficit > 0:

                    grid_power = remaining_deficit


            cost = self.tariff.calculate_cost(
                grid_power,
                hour
            )

            self.total_cost += cost


            self.results.append(
                {
                    "day": day,
                    "hour": hour,
                    "load": load,
                    "solar": solar_power,
                    "battery_soc": self.battery.soc * 100,
                    "grid": grid_power,
                    "cost": cost
                }
            )


    def print_results(self):

        print("\n========== ENERGY SIMULATION ==========\n")

        for result in self.results:

            print(
                f"Day {result['day']} "
                f"{result['hour']:02d}:00 | "
                f"Load: {result['load']:.0f} W | "
                f"Solar: {result['solar']:.0f} W | "
                f"Battery: {result['battery_soc']:.1f}% | "
                f"Grid: {result['grid']:.0f} W | "
                f"Cost: ${result['cost']:.2f}"
            )


        print("\n==============================")
        print(
            f"Total Cost: ${self.total_cost:.2f}"
        )


    def get_dataframe(self):

        return pd.DataFrame(self.results)


    def save_results(self, filename="data/energy_results.csv"):

        df = self.get_dataframe()

        df.to_csv(filename, index=False)

        print(f"Saved results to {filename}")