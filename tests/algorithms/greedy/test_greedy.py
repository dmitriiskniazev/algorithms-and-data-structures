from itertools import combinations

import pytest

from algorithms.greedy import fractional_knapsack, huffman, interval_scheduling


def _compatible(intervals: list[tuple[int, int]], indices: list[int]) -> bool:
    ordered = sorted((intervals[index] for index in indices), key=lambda interval: interval[0])
    return all(left[1] <= right[0] for left, right in zip(ordered, ordered[1:]))


def test_interval_scheduling_returns_maximum_compatible_set() -> None:
    intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    result = interval_scheduling.select(intervals)
    optimum = max(
        (
            len(candidate)
            for size in range(len(intervals) + 1)
            for candidate in combinations(range(len(intervals)), size)
            if _compatible(intervals, list(candidate))
        ),
        default=0,
    )
    assert _compatible(intervals, result)
    assert len(result) == optimum == 4


def test_interval_scheduling_handles_empty_touching_and_invalid_intervals() -> None:
    assert interval_scheduling.select([]) == []
    assert interval_scheduling.select([(1, 2), (2, 2), (2, 3)]) == [0, 1, 2]
    with pytest.raises(ValueError):
        interval_scheduling.select([(3, 2)])


def test_fractional_knapsack_uses_density_and_splits_last_item() -> None:
    assert fractional_knapsack.solve([(10, 60), (20, 100), (30, 120)], 50) == pytest.approx(240)
    assert fractional_knapsack.solve([(4, 12), (2, 4)], 0) == 0
    assert fractional_knapsack.solve([], 10) == 0


@pytest.mark.parametrize(("items", "capacity"), [([(-1, 4)], 1), ([(1, -1)], 1), ([(0, 2)], 1), ([], -1)])
def test_fractional_knapsack_rejects_invalid_input(items: list[tuple[int, int]], capacity: int) -> None:
    with pytest.raises(ValueError):
        fractional_knapsack.solve(items, capacity)


def test_huffman_code_is_prefix_free_and_has_optimal_weighted_length() -> None:
    frequencies = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
    codes = huffman.build_codes(frequencies)
    assert set(codes) == set(frequencies)
    assert all(set(code) <= {"0", "1"} for code in codes.values())
    assert all(left == right or not right.startswith(left) for left in codes.values() for right in codes.values())
    assert sum(frequencies[symbol] * len(code) for symbol, code in codes.items()) == 224
    assert huffman.build_codes({}) == {}
    assert huffman.build_codes({"only": 7}) == {"only": "0"}


def test_huffman_rejects_nonpositive_frequencies() -> None:
    with pytest.raises(ValueError):
        huffman.build_codes({"a": 0})
