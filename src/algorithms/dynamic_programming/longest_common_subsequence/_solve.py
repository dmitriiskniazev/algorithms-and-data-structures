from algorithms.dynamic_programming.longest_common_subsequence._build_parents import build_parents
from algorithms.dynamic_programming.longest_common_subsequence._restore_from_parents import restore_from_parents


def solve(first: str, second: str) -> str:
    _, parent = build_parents(first, second)
    return restore_from_parents(first, second, parent)
