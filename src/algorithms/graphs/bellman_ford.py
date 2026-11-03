from algorithms.graphs._common import WeightedGraph, validate_weighted_graph


def shortest_paths(graph: WeightedGraph, source: int) -> tuple[tuple[int | None, ...], tuple[int | None, ...]]:
    validate_weighted_graph(graph, source)
    dist: list[int | None] = [None] * len(graph)
    parent: list[int | None] = [None] * len(graph)
    dist[source] = 0
    edges = [(u, v, weight) for u, neighbors in enumerate(graph) for v, weight in neighbors]

    for _ in range(max(0, len(graph) - 1)):
        changed = False
        for u, v, weight in edges:
            distance = dist[u]
            if distance is None:
                continue
            candidate = distance + weight
            curr = dist[v]
            if curr is None or candidate < curr:
                dist[v] = candidate
                parent[v] = u
                changed = True
        if not changed:
            break

    for u, v, weight in edges:
        distance, curr = dist[u], dist[v]
        if distance is not None and (curr is None or distance + weight < curr):
            raise ValueError("a negative cycle is reachable from the source")
    return tuple(dist), tuple(parent)
