from bisect import bisect_left
from collections.abc import Sequence

from algorithms.dynamic_programming.longest_increasing_subsequence._types import State


def build_table(values: Sequence[int]) -> tuple[list[int], State | None]:
    dp = [0] * len(values)
    tails: list[int] = []
    end: State | None = None
    for i, x in enumerate(values):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError("values must be integers")
        k = bisect_left(tails, x)
        dp[i] = k + 1
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
        if k == len(tails) - 1:
            end = i
    return dp, end
