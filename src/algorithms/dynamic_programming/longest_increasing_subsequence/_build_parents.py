from bisect import bisect_left
from collections.abc import Sequence

from algorithms.dynamic_programming.longest_increasing_subsequence._types import Parents, State


def build_parents(values: Sequence[int]) -> tuple[int, State | None, Parents]:
    parent: Parents = [None] * len(values)
    tails: list[int] = []
    tail_indices: list[int] = []
    for i, x in enumerate(values):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError("values must be integers")
        k = bisect_left(tails, x)
        parent[i] = tail_indices[k - 1] if k else None
        if k == len(tails):
            tails.append(x)
            tail_indices.append(i)
        else:
            tails[k] = x
            tail_indices[k] = i
    end = tail_indices[-1] if tail_indices else None
    return len(tails), end, parent
