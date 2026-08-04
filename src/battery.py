class Battery:

    def __init__(
        self,
        capacity_kwh=10,
        soc=0.5,
        efficiency=0.95,
        max_charge_kw=3,
        max_discharge_kw=3
    ):

        self.capacity_kwh = capacity_kwh

        self.energy = capacity_kwh * soc

        self.efficiency = efficiency

        self.max_charge_kw = max_charge_kw

        self.max_discharge_kw = max_discharge_kw

    @property
    def soc(self):
        return self.energy / self.capacity_kwh

    def charge(self, power_w):

        power_kw = power_w / 1000

        power_kw = min(power_kw, self.max_charge_kw)

        energy_added = power_kw * self.efficiency

        self.energy = min(
            self.capacity_kwh,
            self.energy + energy_added
        )

    def discharge(self, power_w):

        power_kw = power_w / 1000

        power_kw = min(power_kw, self.max_discharge_kw)

        energy_removed = power_kw / self.efficiency

        energy_removed = min(
            energy_removed,
            self.energy
        )

        self.energy -= energy_removed

        return energy_removed * 1000

    def print_status(self):

        print(f"Battery Energy : {self.energy:.2f} kWh")
        print(f"Battery SoC    : {self.soc*100:.1f}%")