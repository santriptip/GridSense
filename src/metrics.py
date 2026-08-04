class EnergyMetrics:

    def __init__(self, dataframe):
        self.df = dataframe


    def total_load_energy(self):
        """
        Total household energy consumption (kWh)
        """
        return self.df["load"].sum() / 1000


    def total_solar_energy(self):
        """
        Total solar energy generated (kWh)
        """
        return self.df["solar"].sum() / 1000


    def grid_energy_used(self):
        """
        Energy imported from grid (kWh)
        """
        return self.df["grid"].sum() / 1000


    def solar_fraction(self):
        """
        Percentage of demand supplied by solar
        """
        return (
            self.total_solar_energy()
            /
            self.total_load_energy()
        ) * 100


    def total_cost(self):
        """
        Total electricity cost
        """
        return self.df["cost"].sum()