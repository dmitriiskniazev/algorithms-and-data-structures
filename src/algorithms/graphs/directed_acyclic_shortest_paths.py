from algorithms.graphs._common import WeightedGraph, validate_weighted_graph
from algorithms.graphs.topological_sort import sort


def shortest_paths(graph: WeightedGraph, source: int) -> tuple[tuple[int | None, ...], tuple[int | None, ...]]:
    validate_weighted_graph(graph, source)
    order = sort([[v for v, _ in neighbors] for neighbors in graph])
    dist: list[int | None] = [None] * len(graph)
    parent: list[int | None] = [None] * len(graph)
    dist[source] = 0
    for u in order:
        distance = dist[u]
        if distance is None:
            continue
        for v, weight in graph[u]:
            candidate = distance + weight
            curr = dist[v]
            if curr is None or candidate < curr:
                dist[v] = candidate
                parent[v] = u
    return tuple(dist), tuple(parent)
