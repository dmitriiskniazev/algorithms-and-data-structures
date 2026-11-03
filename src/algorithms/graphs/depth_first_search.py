from algorithms.graphs._common import Graph, validate_graph


def traverse(graph: Graph, source: int) -> tuple[int, ...]:
    validate_graph(graph)
    if not 0 <= source < len(graph):
        raise ValueError("source is outside the graph")

    seen = {source}
    order = [source]
    frames = [(source, iter(graph[source]))]
    while frames:
        _, neighbors = frames[-1]
        v = next(neighbors, None)
        if v is None:
            frames.pop()
        elif v not in seen:
            seen.add(v)
            order.append(v)
            frames.append((v, iter(graph[v])))
    return tuple(order)
