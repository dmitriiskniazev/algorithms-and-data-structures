from collections.abc import Iterable

from algorithms.complexity._common import Edge, simple_undirected_edges


def approximate(vertex_count: int, edges: Iterable[Edge]) -> tuple[int, ...]:
    normalized = simple_undirected_edges(vertex_count, edges)
    if normalized is None:
        raise ValueError("expected a simple undirected graph with valid vertices")
    matched: set[int] = set()
    cover: set[int] = set()
    for left, right in sorted(normalized):
        if left not in matched and right not in matched:
            matched.update((left, right))
            cover.update((left, right))
    return tuple(sorted(cover))
