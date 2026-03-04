# dp_model.py

def dp_feasibility(total_demand, sources):
    """
    Checks if total demand can be met
    within source capacity constraints
    """

    dp = {0: 0}  # energy_used : cost

    for source in sources:
        new_dp = dp.copy()
        cap = source["capacity"]
        cost = source["cost"]

        for used, prev_cost in dp.items():
            for e in range(cap + 1):
                total = used + e
                new_cost = prev_cost + e * cost

                if total not in new_dp or new_cost < new_dp[total]:
                    new_dp[total] = new_cost

        dp = new_dp

    return dp
