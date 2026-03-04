from itertools import permutations

def brute_force(spots, max_time, max_budget):
    best = []
    best_count = 0

    for r in permutations(spots):
        time = cost = 0
        temp = []
        for s in r:
            time += s["visit_time"]
            cost += s["fee"]
            if time <= max_time and cost <= max_budget:
                temp.append(s)
        if len(temp) > best_count:
            best = temp
            best_count = len(temp)

    return best
