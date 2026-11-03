from algorithms.graphs._common import WeightedEdge, WeightedGraph
from algorithms.graphs._indexed_heap import IndexedHeap


def minimum_spanning_forest(graph: WeightedGraph) -> tuple[WeightedEdge, ...]:
    n = len(graph)
    _validate(graph)
    best: list[int | None] = [None] * n
    parent: list[int | None] = [None] * n
    included = [False] * n
    heap = IndexedHeap(n)
    forest: list[WeightedEdge] = []
    for root in range(n):
        if included[root]:
            continue
        best[root] = 0
        heap.push_or_decrease(root, 0)
        while heap:
            weight, u = heap.pop()
            if included[u]:
                continue
            included[u] = True
            prev = parent[u]
            if prev is not None:
                forest.append((weight, prev, u))
            for v, edge_weight in graph[u]:
                if included[v]:
                    continue
                curr = best[v]
                if curr is None or edge_weight < curr:
                    best[v] = edge_weight
                    parent[v] = u
                    heap.push_or_decrease(v, edge_weight)
    return tuple(forest)


def _validate(graph: WeightedGraph) -> None:
    n = len(graph)
    for neighbors in graph:
        for v, weight in neighbors:
            if not 0 <= v < n:
                raise ValueError("neighbor is outside the graph")
            if not isinstance(weight, int) or isinstance(weight, bool):
                raise ValueError("edge weights must be integers")
