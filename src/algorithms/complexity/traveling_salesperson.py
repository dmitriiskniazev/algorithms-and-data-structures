from collections.abc import Sequence

from algorithms.complexity._common import TourMatrix, _is_nonnegative_int


def verify(weights: TourMatrix, tour: Sequence[int], bound: int) -> bool:
    n = len(weights)
    if not _is_nonnegative_int(bound) or n == 0:
        return False
    if any(len(row) != n for row in weights):
        return False
    if any(edge is not None and not _is_nonnegative_int(edge) for row in weights for edge in row):
        return False
    try:
        vertices = tuple(tour)
    except TypeError:
        return False
    if len(vertices) != n or any(not _is_nonnegative_int(vertex) or vertex >= n for vertex in vertices):
        return False
    if len(set(vertices)) != n:
        return False
    total = 0
    for i, source in enumerate(vertices):
        destination = vertices[(i + 1) % n]
        edge = weights[source][destination]
        if edge is None:
            return False
        total += edge
        if total > bound:
            return False
    return True
