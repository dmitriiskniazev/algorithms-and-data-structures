from algorithms.graphs._common import Graph, validate_graph


def exists(graph: Graph) -> bool:
    validate_graph(graph)
    state = [0] * len(graph)
    for source in range(len(graph)):
        if state[source] != 0:
            continue
        state[source] = 1
        frames = [(source, 0)]
        while frames:
            u, i = frames[-1]
            if i == len(graph[u]):
                state[u] = 2
                frames.pop()
                continue
            frames[-1] = (u, i + 1)
            v = graph[u][i]
            if state[v] == 1:
                return True
            if state[v] == 0:
                state[v] = 1
                frames.append((v, 0))
    return False
