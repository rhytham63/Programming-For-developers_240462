# main.py

from T1 import demand_data, energy_sources
from t3 import greedy_hourly_allocation

hour = 6

result = greedy_hourly_allocation(hour, demand_data, energy_sources)

print(f"Energy Allocation for Hour {hour}")
for source, values in result.items():
    print(source, values)
