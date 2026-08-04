class Appliance:
    def __init__(self, name, rated_power, priority, duty_cycle, schedule):
        self.name = name
        self.rated_power = rated_power      # Watts
        self.priority = priority            # High, Medium, Low
        self.duty_cycle = duty_cycle        # 0.0 - 1.0
        self.schedule = schedule            # List of 24 values (0 or 1)

    def get_power(self, hour):
        if self.schedule[hour]:
            return self.rated_power * self.duty_cycle
        return 0

    def __str__(self):
        return (
            f"{self.name}: "
            f"{self.rated_power} W | "
            f"Duty Cycle: {self.duty_cycle} | "
            f"Priority: {self.priority}"
        )


class House:
    def __init__(self):

        self.appliances = [

            Appliance(
                "Lights",
                80,
                "High",
                1.0,
                [
                    0,0,0,0,0,0,
                    0,0,0,0,0,0,
                    0,0,0,0,0,0,
                    1,1,1,1,1,0
                ]
            ),

            Appliance(
                "Fan",
                75,
                "Medium",
                1.0,
                [
                    1,1,1,1,1,1,
                    0,0,0,0,0,0,
                    0,0,0,0,0,0,
                    1,1,1,1,1,1
                ]
            ),

            Appliance(
                "Refrigerator",
                200,
                "High",
                0.35,
                [1] * 24
            ),

            Appliance(
                "TV",
                120,
                "Low",
                1.0,
                [
                    0,0,0,0,0,0,
                    0,0,0,0,0,0,
                    0,0,0,0,0,0,
                    0,1,1,1,0,0
                ]
            ),

            Appliance(
                "Air Conditioner",
                1500,
                "Low",
                0.8,
                [
                    0,0,0,0,0,0,
                    0,0,0,0,0,0,
                    1,1,1,1,1,0,
                    0,0,1,1,1,0
                ]
            )
        ]

    def display_appliances(self):
        print("\n========== APPLIANCES ==========\n")

        for appliance in self.appliances:
            print(appliance)

    def get_total_load(self, hour):
        total = 0

        for appliance in self.appliances:
            total += appliance.get_power(hour)

        return total

    def print_daily_load(self):

        print("\n========== DAILY LOAD ==========\n")

        for hour in range(24):
            load = self.get_total_load(hour)

            print(f"{hour:02d}:00   {load:.1f} W")