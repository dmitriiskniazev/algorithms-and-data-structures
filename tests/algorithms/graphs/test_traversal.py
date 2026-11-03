import pytest

from algorithms.graphs import (
    bipartite,
    breadth_first_search,
    connected_components,
    depth_first_search,
    directed_cycle,
    topological_sort,
    undirected_cycle,
)


def test_bfs_returns_shortest_paths_and_marks_unreachable_vertices():
    graph = [[1, 2], [0, 3], [0, 3], [1, 2], [], []]
    distances, predecessors = breadth_first_search.traverse(graph, 0)
    assert distances == (0, 1, 1, 2, None, None)
    assert predecessors == (None, 0, 0, 1, None, None)


def test_dfs_is_iterative_and_respects_neighbor_order():
    graph = [[1, 2], [3], [3], [], []]
    assert depth_first_search.traverse(graph, 0) == (0, 1, 3, 2)
    assert depth_first_search.traverse([[]] * 5000, 4999) == (4999,)


def test_components_include_isolated_vertices_and_partition_graph():
    assert connected_components.find([[1], [0, 2], [1], [], [5], [4]]) == ((0, 1, 2), (3,), (4, 5))
    assert connected_components.find([]) == ()


@pytest.mark.parametrize(
    ("graph", "expected"), [([[1], [0, 2], [1]], True), ([[1, 2], [0, 2], [0, 1]], False), ([[0]], False)]
)
def test_bipartiteness(graph, expected):
    assert bipartite.check(graph) is expected


@pytest.mark.parametrize(
    ("graph", "expected"),
    [([[]], False), ([[1], [0]], False), ([[1, 1], [0, 0]], True), ([[1, 2], [0, 2], [0, 1]], True)],
)
def test_undirected_cycle_detection(graph, expected):
    assert undirected_cycle.exists(graph) is expected


def test_undirected_algorithms_reject_asymmetric_adjacency():
    with pytest.raises(ValueError, match="multiplicity"):
        connected_components.find([[1], []])


def test_directed_cycle_detection_and_topological_order():
    dag = [[1, 2], [3], [3], [], []]
    assert not directed_cycle.exists(dag)
    order = topological_sort.sort(dag)
    positions = {vertex: index for index, vertex in enumerate(order)}
    assert sorted(order) == list(range(len(dag)))
    assert all(positions[u] < positions[v] for u, ns in enumerate(dag) for v in ns)
    assert topological_sort.sort([]) == ()
    assert directed_cycle.exists([[1], [2], [0]])
    assert directed_cycle.exists([[0]])
    with pytest.raises(ValueError, match="cyclic"):
        topological_sort.sort([[0]])


def test_invalid_vertices_are_rejected():
    with pytest.raises(ValueError, match="source"):
        breadth_first_search.traverse([[]], 1)
    with pytest.raises(ValueError, match="neighbor"):
        depth_first_search.traverse([[1]], 0)
