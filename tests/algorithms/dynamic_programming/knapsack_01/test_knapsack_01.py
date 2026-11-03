from algorithms.dynamic_programming import knapsack_01


def test_knapsack_reconstructs_optimal_feasible_indices() -> None:
    value, chosen = knapsack_01.solve([2, 3, 4, 0], [3, 4, 5, 2], 5)
    assert value == 9
    assert len(chosen) == len(set(chosen))
    assert sum([2, 3, 4, 0][i] for i in chosen) <= 5
    assert sum([3, 4, 5, 2][i] for i in chosen) == value


def test_knapsack_omits_negative_values_and_handles_zero_capacity() -> None:
    assert knapsack_01.solve([0, 1], [-1, 10], 0) == (0, [])
    assert knapsack_01.solve([0, 2], [4, 9], 0) == (4, [0])


def test_knapsack_empty_input() -> None:
    assert knapsack_01.solve([], [], 0) == (0, [])
    assert knapsack_01.solve([], [], 5) == (0, [])
