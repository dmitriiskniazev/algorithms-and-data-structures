from collections.abc import Iterable, Sequence

type Edge = tuple[int, int]


type TourMatrix = Sequence[Sequence[int | None]]


def _is_nonnegative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def simple_undirected_edges(vertex_count: int, edges: Iterable[Edge]) -> set[tuple[int, int]] | None:
    if not _is_nonnegative_int(vertex_count):
        return None
    normalized: set[tuple[int, int]] = set()
    try:
        for edge in edges:
            if len(edge) != 2:
                return None
            left, right = edge
            if (
                not _is_nonnegative_int(left)
                or not _is_nonnegative_int(right)
                or left >= vertex_count
                or right >= vertex_count
                or left == right
            ):
                return None
            normalized.add((min(left, right), max(left, right)))
    except TypeError, ValueError:
        return None
    return normalized
