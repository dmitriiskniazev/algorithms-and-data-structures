from collections import deque
from typing import cast

from algorithms.graphs._common import Graph, validate_graph


def traverse(graph: Graph, source: int) -> tuple[tuple[int | None, ...], tuple[int | None, ...]]:
    validate_graph(graph)
    if not 0 <= source < len(graph):
        raise ValueError("source is outside the graph")

    dist: list[int | None] = [None] * len(graph)
    parent: list[int | None] = [None] * len(graph)
    dist[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if dist[v] is None:
                dist[v] = cast(int, dist[u]) + 1
                parent[v] = u
                queue.append(v)
    return tuple(dist), tuple(parent)
