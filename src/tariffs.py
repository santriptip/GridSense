class Tariff:
    """
    Electricity pricing model.
    """

    def __init__(
        self,
        peak_price=0.40,
        off_peak_price=0.20,
        peak_hours=None
    ):

        self.peak_price = peak_price
        self.off_peak_price = off_peak_price

        if peak_hours is None:
            self.peak_hours = [
                17, 18, 19, 20, 21
            ]
        else:
            self.peak_hours = peak_hours


    def get_price(self, hour):
        """
        Returns electricity price in $/kWh
        """

        if hour in self.peak_hours:
            return self.peak_price

        return self.off_peak_price


    def calculate_cost(self, power_w, hour):
        """
        Calculates cost for one hour.

        power_w = watts consumed from grid
        """

        energy_kwh = power_w / 1000

        price = self.get_price(hour)

        return energy_kwh * price