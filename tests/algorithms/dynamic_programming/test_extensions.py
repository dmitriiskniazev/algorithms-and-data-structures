from itertools import pairwise

import pytest

from algorithms.dynamic_programming import (
    longest_increasing_subsequence,
    matrix_chain_order,
    weighted_interval_scheduling,
)


def test_weighted_interval_scheduling_reconstructs_optimum_and_touching_is_compatible() -> None:
    intervals = [(0, 3, 5), (3, 5, 6), (1, 4, 20), (8, 8, 4), (8, 8, -1)]
    weight, indices = weighted_interval_scheduling.solve(intervals)
    assert weight == 24
    assert indices == [2, 3]


def test_weighted_interval_scheduling_empty_negative_and_ties() -> None:
    assert weighted_interval_scheduling.solve([]) == (0, [])
    assert weighted_interval_scheduling.solve([(0, 1, -2), (1, 2, 0)]) == (0, [])
    assert weighted_interval_scheduling.solve([(0, 2, 4), (0, 2, 4)]) == (4, [0])


def test_weighted_interval_scheduling_validates_intervals() -> None:
    with pytest.raises(ValueError):
        weighted_interval_scheduling.solve([(2, 1, 3)])
    with pytest.raises(ValueError):
        weighted_interval_scheduling.solve([(0, 1, True)])


@pytest.mark.parametrize(
    "values, expected_length", [([], 0), ([4, 4, 4], 1), ([-5, -1, -3, 0], 3), ([1, 2, 3, 4], 4), ([4, 3, 2, 1], 1)]
)
def test_lis_contract(values: list[int], expected_length: int) -> None:
    sequence, indices = longest_increasing_subsequence.solve(values)
    assert len(sequence) == len(indices) == expected_length
    assert [values[i] for i in indices] == sequence
    assert all(a < b for a, b in pairwise(sequence))
    assert all(a < b for a, b in pairwise(indices))


def test_lis_multiple_optima_and_invalid_values() -> None:
    sequence, indices = longest_increasing_subsequence.solve([3, 1, 2, 1, 2, 4])
    assert sequence == [1, 2, 4]
    assert len(indices) == 3
    with pytest.raises(TypeError):
        longest_increasing_subsequence.solve([1, True])


def test_matrix_chain_classic_singleton_and_tie() -> None:
    assert matrix_chain_order.solve([30, 35, 15, 5, 10, 20, 25]) == (15125, "((A1*(A2*A3))*((A4*A5)*A6))")
    assert matrix_chain_order.solve([7, 11]) == (0, "A1")
    assert matrix_chain_order.solve([2, 2, 2, 2]) == (16, "(A1*(A2*A3))")


def test_matrix_chain_validates_empty_and_nonpositive_dimensions() -> None:
    with pytest.raises(ValueError):
        matrix_chain_order.solve([])
    with pytest.raises(ValueError):
        matrix_chain_order.solve([2, 0])
    with pytest.raises(ValueError):
        matrix_chain_order.solve([2, True])
