from collections import Counter
from collections.abc import Sequence

type Graph = Sequence[Sequence[int]]


def validate_graph(graph: Graph) -> None:
    n = len(graph)
    for neighbors in graph:
        for v in neighbors:
            if not 0 <= v < n:
                raise ValueError(f"neighbor {v} is outside 0..{n - 1}")


def validate_undirected(graph: Graph) -> None:
    validate_graph(graph)
    counts = [Counter(neighbors) for neighbors in graph]
    for u, row in enumerate(counts):
        for v, count in row.items():
            if count != counts[v][u]:
                raise ValueError("undirected edges must occur with equal multiplicity")


type WeightedGraph = Sequence[Sequence[tuple[int, int]]]


type WeightedEdge = tuple[int, int, int]


def validate_weighted_graph(graph: WeightedGraph, source: int) -> None:
    n = len(graph)
    if not 0 <= source < n:
        raise ValueError("source is outside the graph")
    for neighbors in graph:
        for v, weight in neighbors:
            if not 0 <= v < n:
                raise ValueError("neighbor is outside the graph")
            if not isinstance(weight, int) or isinstance(weight, bool):
                raise ValueError("edge weights must be integers")
