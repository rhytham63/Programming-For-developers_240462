import heapq
import math

def safest_path_dijkstra(graph, source):
    """
    Finds the safest path (maximum probability path)
    from 'source' to all other nodes using Dijkstra
    with -log transformation.
    """

    # Initialize distances and previous nodes
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0.0

    # Min-heap priority queue
    priority_queue = [(0.0, source)]

    while priority_queue:
        d_u, u = heapq.heappop(priority_queue)

        # Skip stale entries
        if d_u > dist[u]:
            continue

        for v, p_uv in graph[u]:

            # Avoid log(0) error
            if p_uv <= 0:
                continue

            # Transform weight
            w_prime = -math.log(p_uv)
            new_dist = dist[u] + w_prime

            # Relaxation step
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(priority_queue, (new_dist, v))

    return dist, prev


def reconstruct_path(prev, source, target):
    """Reconstruct path from source to target"""
    path = []
    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path
    return []


# -------- Graph Definition --------
graph = {
    'KTM': [('JA', 0.90), ('JB', 0.80)],
    'JA':  [('KTM', 0.90), ('PH', 0.95), ('BS', 0.70)],
    'JB':  [('KTM', 0.80), ('JA', 0.60), ('BS', 0.90)],
    'PH':  [('JA', 0.95), ('BS', 0.85)],
    'BS':  [('JA', 0.70), ('JB', 0.90), ('PH', 0.85)],
}


# -------- Run Algorithm --------
source_node = 'KTM'
dist, prev = safest_path_dijkstra(graph, source_node)

print(f"Safest Paths from {source_node}:\n")

for node in graph:
    if node == source_node:
        continue

    path = reconstruct_path(prev, source_node, node)

    if path:
        safety = math.exp(-dist[node])  # Convert back to probability
        print(f"{source_node} -> {node}: {' -> '.join(path)}")
        print(f"Safety Probability = {safety:.4f}\n")
    else:
        print(f"No path to {node}\n")