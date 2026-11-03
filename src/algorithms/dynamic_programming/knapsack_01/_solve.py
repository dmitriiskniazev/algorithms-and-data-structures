from collections.abc import Sequence

from algorithms.dynamic_programming.knapsack_01._build_parents import build_parents
from algorithms.dynamic_programming.knapsack_01._restore_from_parents import restore_from_parents


def solve(weights: Sequence[int], values: Sequence[int], capacity: int) -> tuple[int, list[int]]:
    val, parent = build_parents(weights, values, capacity)
    return val, restore_from_parents(weights, capacity, parent)
