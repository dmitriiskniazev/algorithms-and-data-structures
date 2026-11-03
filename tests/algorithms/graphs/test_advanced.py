import pytest

from algorithms.graphs import (
    bellman_ford,
    dijkstra,
    directed_acyclic_shortest_paths,
    floyd_warshall,
    kruskal,
    prim,
    strongly_connected_components,
)


def _reachable(graph: list[list[int]], source: int) -> set[int]:
    reached = {source}
    stack = [source]
    while stack:
        vertex = stack.pop()
        for neighbor in graph[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                stack.append(neighbor)
    return reached


def test_kosaraju_returns_maximal_components_and_covers_vertices():
    graph = [[1], [2], [0, 3], [4], [3], [], [5]]
    components = strongly_connected_components.find(graph)
    assert {frozenset(component) for component in components} == {
        frozenset({0, 1, 2}),
        frozenset({3, 4}),
        frozenset({5}),
        frozenset({6}),
    }
    assert sorted(vertex for component in components for vertex in component) == list(range(7))
    reachability = [_reachable(graph, vertex) for vertex in range(len(graph))]
    for component in components:
        for first in component:
            for second in component:
                assert second in reachability[first]
                assert first in reachability[second]
    assert strongly_connected_components.find([]) == ()


def test_kosaraju_is_iterative_for_deep_graphs():
    size = 6000
    graph = [[vertex + 1] if vertex + 1 < size else [] for vertex in range(size)]
    components = strongly_connected_components.find(graph)
    assert len(components) == size
    assert sum(map(len, components)) == size


def test_dijkstra_zero_weights_paths_and_unreachable_vertices():
    graph = [[(1, 0), (2, 7)], [(2, 2), (3, 5)], [(3, 1)], [], []]
    distances, predecessors = dijkstra.shortest_paths(graph, 0)
    assert distances == (0, 0, 2, 3, None)
    assert predecessors == (None, 0, 1, 2, None)


def test_dijkstra_rejects_negative_weight_and_invalid_vertices():
    with pytest.raises(ValueError, match="nonnegative"):
        dijkstra.shortest_paths([[(1, 2)], [(0, -1)]], 0)
    with pytest.raises(ValueError, match="neighbor"):
        dijkstra.shortest_paths([[(2, 1)]], 0)


def test_bellman_ford_handles_negative_edges_and_unreachable_negative_cycle():
    graph = [[(1, 4), (2, 5)], [(2, -3), (3, 4)], [(3, 2)], [], [(5, -2)], [(4, 1)]]
    distances, predecessors = bellman_ford.shortest_paths(graph, 0)
    assert distances == (0, 4, 1, 3, None, None)
    assert predecessors == (None, 0, 1, 2, None, None)


def test_bellman_ford_reports_reachable_negative_cycle():
    with pytest.raises(ValueError, match="negative cycle"):
        bellman_ford.shortest_paths([[(1, 1)], [(2, -3)], [(1, 1)]], 0)
    with pytest.raises(ValueError, match="source"):
        bellman_ford.shortest_paths([[]], 1)


def test_dag_shortest_paths_allow_negative_weights_and_reject_cycles():
    graph = [[(1, 4), (2, 5)], [(2, -3), (3, 4)], [(3, 2)], [], []]
    assert directed_acyclic_shortest_paths.shortest_paths(graph, 0) == ((0, 4, 1, 3, None), (None, 0, 1, 2, None))
    with pytest.raises(ValueError, match="cyclic"):
        directed_acyclic_shortest_paths.shortest_paths([[(1, 1)], [(0, 1)]], 0)


def test_floyd_warshall_computes_all_pairs_and_detects_negative_cycle():
    infinity = None
    matrix = [
        [0, 3, 10, infinity],
        [infinity, 0, -2, infinity],
        [infinity, infinity, 0, 4],
        [infinity, infinity, infinity, 0],
    ]
    assert floyd_warshall.shortest_paths(matrix) == (
        (0, 3, 1, 5),
        (None, 0, -2, 2),
        (None, None, 0, 4),
        (None, None, None, 0),
    )
    with pytest.raises(ValueError, match="negative cycle"):
        floyd_warshall.shortest_paths([[0, -1], [0, 0]])
    with pytest.raises(ValueError, match="square"):
        floyd_warshall.shortest_paths([[0, 1]])


def test_kruskal_handles_loops_parallel_edges_ties_and_disconnected_graph():
    edges = [(8, 0, 0), (4, 0, 1), (1, 0, 1), (2, 1, 2), (2, 0, 2), (-3, 3, 4)]
    forest = kruskal.minimum_spanning_forest(6, edges)
    assert len(forest) == 3
    assert sum(weight for weight, _, _ in forest) == 0
    assert set(forest) == {(1, 0, 1), (2, 0, 2), (-3, 3, 4)}
    assert kruskal.minimum_spanning_forest(0, []) == ()


def test_kruskal_rejects_invalid_endpoints():
    with pytest.raises(ValueError, match="endpoint"):
        kruskal.minimum_spanning_forest(2, [(1, 0, 2)])


def test_prim_returns_minimum_forest_with_negative_weights_and_parallel_edges():
    graph = [[(0, 0), (1, 1), (1, 4), (2, 2)], [(0, 1), (0, 4), (2, -2)], [(0, 2), (1, -2)], [(4, -3)], [(3, -3)], []]
    forest = prim.minimum_spanning_forest(graph)
    assert len(forest) == 3
    assert sum(weight for weight, _, _ in forest) == -4
    assert prim.minimum_spanning_forest([]) == ()


def test_prim_rejects_invalid_vertices():
    with pytest.raises(ValueError, match="neighbor"):
        prim.minimum_spanning_forest([[(2, 1)]])
