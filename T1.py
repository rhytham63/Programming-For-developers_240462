# data.py

# Hourly demand in kWh
demand_data = {
    6: {"A": 20, "B": 15, "C": 25}
}

# Energy source information
energy_sources = {
    "Solar": {
        "capacity": 50,
        "available_hours": range(6, 19),
        "cost": 1.0,
        "renewable": True
    },
    "Hydro": {
        "capacity": 40,
        "available_hours": range(0, 24),
        "cost": 1.5,
        "renewable": True
    },
    "Diesel": {
        "capacity": 60,
        "available_hours": range(17, 24),
        "cost": 3.0,
        "renewable": False
    }
}
