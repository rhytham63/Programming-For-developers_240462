def check_demand_tolerance(demand, supplied):
    """
    Checks if supplied energy is within ±10% of demand
    """
    lower_limit = 0.9 * demand
    upper_limit = 1.1 * demand

    return lower_limit <= supplied <= upper_limit
