from algorithms.graphs._common import WeightedGraph, validate_weighted_graph
from algorithms.graphs._indexed_heap import IndexedHeap


def shortest_paths(graph: WeightedGraph, source: int) -> tuple[tuple[int | None, ...], tuple[int | None, ...]]:
    validate_weighted_graph(graph, source)
    if any(weight < 0 for neighbors in graph for _, weight in neighbors):
        raise ValueError("Dijkstra requires nonnegative edge weights")
    dist: list[int | None] = [None] * len(graph)
    parent: list[int | None] = [None] * len(graph)
    dist[source] = 0
    heap = IndexedHeap(len(graph))
    heap.push_or_decrease(source, 0)
    while heap:
        distance, u = heap.pop()
        for v, weight in graph[u]:
            candidate = distance + weight
            curr = dist[v]
            if curr is None or candidate < curr:
                dist[v] = candidate
                parent[v] = u
                heap.push_or_decrease(v, candidate)
    return tuple(dist), tuple(parent)
