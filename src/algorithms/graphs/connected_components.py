from algorithms.graphs._common import Graph, validate_undirected


def find(graph: Graph) -> tuple[tuple[int, ...], ...]:
    validate_undirected(graph)
    seen = [False] * len(graph)
    components: list[tuple[int, ...]] = []
    for source in range(len(graph)):
        if seen[source]:
            continue
        seen[source] = True
        component: list[int] = []
        frames = [(source, 0)]
        while frames:
            u, i = frames[-1]
            if i == len(graph[u]):
                frames.pop()
                continue
            frames[-1] = (u, i + 1)
            v = graph[u][i]
            if not seen[v]:
                seen[v] = True
                component.append(v)
                frames.append((v, 0))
        components.append((source, *component))
    return tuple(components)
