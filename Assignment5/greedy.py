def greedy_itinerary(spots, max_time, max_budget, interests):
    scored = []

    for s in spots:
        match = len(set(s["tags"]) & interests)
        score = match * 10 - (s["fee"] / 100)
        scored.append((score, s))

    scored.sort(reverse=True, key=lambda x: x[0])

    itinerary = []
    total_time = total_cost = 0

    for _, s in scored:
        if total_time + s["visit_time"] <= max_time and total_cost + s["fee"] <= max_budget:
            itinerary.append(s)
            total_time += s["visit_time"]
            total_cost += s["fee"]

    return itinerary, total_time, total_cost
