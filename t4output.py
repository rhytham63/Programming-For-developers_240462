from t4 import check_demand_tolerance
demand = 20
supplied = 19

if check_demand_tolerance(demand, supplied):
    print("Demand satisfied within tolerance")
else:
    print("Demand not satisfied")
