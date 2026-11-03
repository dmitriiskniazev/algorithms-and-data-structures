from collections.abc import Sequence

from algorithms.graphs._common import WeightedEdge
from data_structures.disjoint_set_union import DisjointSetUnion


def minimum_spanning_forest(vertex_count: int, edges: Sequence[WeightedEdge]) -> tuple[WeightedEdge, ...]:
    if vertex_count < 0:
        raise ValueError("vertex_count must be nonnegative")
    for weight, u, v in edges:
        if not isinstance(weight, int) or isinstance(weight, bool):
            raise ValueError("edge weights must be integers")
        if not 0 <= u < vertex_count or not 0 <= v < vertex_count:
            raise ValueError("edge endpoint is outside the graph")

    dsu = DisjointSetUnion(vertex_count)
    forest: list[WeightedEdge] = []
    for edge in sorted(edges):
        weight, u, v = edge
        if dsu.union(u, v):
            forest.append(edge)
    return tuple(forest)
