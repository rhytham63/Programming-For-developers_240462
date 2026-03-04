# greedy_alloc.py

def greedy_hourly_allocation(hour, demand_data, energy_sources):
    allocation = {}
    remaining_demand = demand_data[hour].copy()

    available_sources = {
        name: src for name, src in energy_sources.items()
        if hour in src["available_hours"]
    }

    sorted_sources = sorted(
        available_sources.items(),
        key=lambda x: x[1]["cost"]
    )

    for source in energy_sources:
        allocation[source] = {"A": 0, "B": 0, "C": 0}

    for source_name, source in sorted_sources:
        capacity_left = source["capacity"]

        for district in remaining_demand:
            if remaining_demand[district] == 0 or capacity_left == 0:
                continue

            supply = min(remaining_demand[district], capacity_left)
            allocation[source_name][district] = supply
            remaining_demand[district] -= supply
            capacity_left -= supply

    return allocation
