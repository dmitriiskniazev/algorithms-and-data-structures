from collections import deque

from algorithms.graphs._common import Graph, validate_undirected


def check(graph: Graph) -> bool:
    validate_undirected(graph)
    colors: list[bool | None] = [None] * len(graph)
    for source in range(len(graph)):
        if colors[source] is not None:
            continue
        colors[source] = False
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if colors[v] is None:
                    colors[v] = not colors[u]
                    queue.append(v)
                elif colors[v] == colors[u]:
                    return False
    return True
