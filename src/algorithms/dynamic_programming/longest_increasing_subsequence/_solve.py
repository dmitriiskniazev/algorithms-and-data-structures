from collections.abc import Sequence

from algorithms.dynamic_programming.longest_increasing_subsequence._build_parents import build_parents
from algorithms.dynamic_programming.longest_increasing_subsequence._restore_from_parents import restore_from_parents


def solve(values: Sequence[int]) -> tuple[list[int], list[int]]:
    _, end, parent = build_parents(values)
    indices = restore_from_parents(end, parent)
    return [values[i] for i in indices], indices
