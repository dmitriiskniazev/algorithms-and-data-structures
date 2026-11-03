from collections.abc import Sequence
from typing import cast


def shortest_paths(distances: Sequence[Sequence[int | None]]) -> tuple[tuple[int | None, ...], ...]:
    n = len(distances)
    if any(len(row) != n for row in distances):
        raise ValueError("distance matrix must be square")
    dist = [list(row) for row in distances]
    if any(
        value is not None and (not isinstance(value, int) or isinstance(value, bool)) for row in dist for value in row
    ):
        raise ValueError("distances must be integers or None")
    for u in range(n):
        diagonal = dist[u][u]
        if diagonal is None or diagonal > 0:
            dist[u][u] = 0
    for k in range(n):
        for u in range(n):
            left = dist[u][k]
            if left is None:
                continue
            for v in range(n):
                right = dist[k][v]
                if right is None:
                    continue
                candidate = left + right
                curr = dist[u][v]
                if curr is None or candidate < curr:
                    dist[u][v] = candidate
    if any(cast(int, dist[u][u]) < 0 for u in range(n)):
        raise ValueError("graph contains a negative cycle")
    return tuple(tuple(row) for row in dist)
