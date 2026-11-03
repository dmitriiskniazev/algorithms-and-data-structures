from collections.abc import Iterable, Sequence

from algorithms.complexity._common import Edge, _is_nonnegative_int, simple_undirected_edges


def verify(vertex_count: int, edges: Iterable[Edge], certificate: Sequence[int], k: int) -> bool:
    normalized = simple_undirected_edges(vertex_count, edges)
    if normalized is None or not _is_nonnegative_int(k):
        return False
    try:
        vertices = tuple(certificate)
    except TypeError:
        return False
    if len(vertices) > k or any(not _is_nonnegative_int(vertex) or vertex >= vertex_count for vertex in vertices):
        return False
    if len(set(vertices)) != len(vertices):
        return False
    selected = set(vertices)
    return all(left in selected or right in selected for left, right in normalized)
