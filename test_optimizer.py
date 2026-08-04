from src.optimizer import optimize_battery


results = optimize_battery(
    solar_capacity_kw=5,
    battery_options=[
        0,
        5,
        10,
        15,
        20
    ]
)

print(results)