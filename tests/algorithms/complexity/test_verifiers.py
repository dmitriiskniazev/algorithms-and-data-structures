from algorithms.complexity import clique, subset_sum, traveling_salesperson, vertex_cover


def test_clique_verifier_checks_size_indices_duplicates_and_edges() -> None:
    edges = [(0, 1), (1, 2), (0, 2), (2, 3)]
    assert clique.verify(4, edges, [0, 1, 2], 3)
    assert not clique.verify(4, edges, [0, 1], 3)
    assert not clique.verify(4, edges, [0, 1, 1], 3)
    assert not clique.verify(4, edges, [0, 1, 4], 3)
    assert not clique.verify(4, edges, [0, 1, 3], 3)
    assert not clique.verify(4, edges, [0, 1, 2], 5)
    assert clique.verify(3, [(0, 1), (1, 0)], [0, 1], 2)


def test_vertex_cover_verifier_requires_every_edge_and_distinct_vertices() -> None:
    edges = [(0, 1), (1, 2), (2, 3)]
    assert vertex_cover.verify(4, edges, [1, 2], 2)
    assert not vertex_cover.verify(4, edges, [0], 1)
    assert not vertex_cover.verify(4, edges, [1, 1], 2)
    assert not vertex_cover.verify(4, edges, [1, 4], 2)
    assert vertex_cover.verify(4, edges, [0, 1, 2, 3], 10)
    assert vertex_cover.verify(4, [], [], 0)


def test_subset_sum_verifier_checks_exact_sum_and_distinct_valid_indices() -> None:
    assert subset_sum.verify([3, 7, 11], 10, [0, 1])
    assert not subset_sum.verify([3, 7, 11], 11, [0, 1])
    assert not subset_sum.verify([3, 7, 11], 6, [0, 0])
    assert not subset_sum.verify([3, 7, 11], 3, [3])
    assert not subset_sum.verify([3, -1], 2, [0, 1])
    assert subset_sum.verify([10**100, 1], 10**100, [0])


def test_tsp_verifier_checks_cycle_edges_cost_and_threshold() -> None:
    matrix = [[None, 2, None], [None, None, 3], [4, None, None]]
    assert traveling_salesperson.verify(matrix, [0, 1, 2], 9)
    assert not traveling_salesperson.verify(matrix, [0, 1, 2], 8)
    assert not traveling_salesperson.verify(matrix, [0, 2, 1], 100)
    assert not traveling_salesperson.verify(matrix, [0, 1, 1], 100)
    assert not traveling_salesperson.verify(matrix, [0, 1], 100)
    assert not traveling_salesperson.verify([[0, 2], [2]], [0, 1], 4)
    assert traveling_salesperson.verify([[0]], [0], 0)


def test_boolean_is_not_accepted_as_an_integer_certificate_field() -> None:
    assert not clique.verify(2, [(0, 1)], [False, 1], 2)
    assert not subset_sum.verify([1], True, [0])
    assert not traveling_salesperson.verify([[0]], [False], 0)


def test_vertex_cover_two_approx_is_a_cover_with_factor_at_most_two() -> None:
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    cover = vertex_cover.approximate(4, edges)
    assert vertex_cover.verify(4, edges, cover, len(cover))
    optimum = min(
        mask.bit_count()
        for mask in range(1 << 4)
        if all(mask & (1 << left) or mask & (1 << right) for left, right in edges)
    )
    assert len(cover) <= 2 * optimum
