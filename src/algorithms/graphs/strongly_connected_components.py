from collections.abc import Sequence


def find(graph: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    n = len(graph)
    for neighbors in graph:
        if any(not 0 <= v < n for v in neighbors):
            raise ValueError("neighbor is outside the graph")

    seen = [False] * n
    finish_order: list[int] = []
    for source in range(n):
        if seen[source]:
            continue
        seen[source] = True
        frames = [(source, 0)]
        while frames:
            u, i = frames[-1]
            if i == len(graph[u]):
                finish_order.append(u)
                frames.pop()
                continue
            frames[-1] = (u, i + 1)
            v = graph[u][i]
            if not seen[v]:
                seen[v] = True
                frames.append((v, 0))

    transpose: list[list[int]] = [[] for _ in range(n)]
    for u, neighbors in enumerate(graph):
        for v in neighbors:
            transpose[v].append(u)

    assigned = [False] * n
    components: list[tuple[int, ...]] = []
    for source in reversed(finish_order):
        if assigned[source]:
            continue
        assigned[source] = True
        component: list[int] = []
        stack = [source]
        while stack:
            u = stack.pop()
            component.append(u)
            for v in transpose[u]:
                if not assigned[v]:
                    assigned[v] = True
                    stack.append(v)
        components.append(tuple(component))
    return tuple(components)
