from algorithms.graphs._common import Graph, validate_undirected


def exists(graph: Graph) -> bool:
    validate_undirected(graph)
    seen = [False] * len(graph)
    for source in range(len(graph)):
        if seen[source]:
            continue
        seen[source] = True
        # Frames retain whether one copy of the parent edge has been skipped.
        frames = [[source, 0, -1, 0]]
        while frames:
            u, i, parent, parent_seen = frames[-1]
            if i == len(graph[u]):
                frames.pop()
                continue
            frames[-1][1] += 1
            v = graph[u][i]
            if v == parent and not parent_seen:
                frames[-1][3] = 1
            elif seen[v]:
                return True
            else:
                seen[v] = True
                frames.append([v, 0, u, 0])
    return False
