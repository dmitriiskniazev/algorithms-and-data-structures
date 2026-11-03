from algorithms.graphs._common import Graph, validate_graph


def sort(graph: Graph) -> tuple[int, ...]:
    validate_graph(graph)
    state = [0] * len(graph)
    order: list[int] = []
    for source in range(len(graph)):
        if state[source] != 0:
            continue
        state[source] = 1
        frames = [(source, 0)]
        while frames:
            u, i = frames[-1]
            if i == len(graph[u]):
                state[u] = 2
                order.append(u)
                frames.pop()
                continue
            frames[-1] = (u, i + 1)
            v = graph[u][i]
            if state[v] == 1:
                raise ValueError("topological order does not exist for cyclic graph")
            if state[v] == 0:
                state[v] = 1
                frames.append((v, 0))
    return tuple(reversed(order))
