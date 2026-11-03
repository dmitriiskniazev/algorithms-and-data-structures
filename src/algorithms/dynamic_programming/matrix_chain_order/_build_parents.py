from collections.abc import Sequence

from algorithms.dynamic_programming.matrix_chain_order._common import cost_of_split
from algorithms.dynamic_programming.matrix_chain_order._types import Parents


def build_parents(dimensions: Sequence[int]) -> tuple[int, Parents]:
    if len(dimensions) < 2:
        raise ValueError("at least one matrix (two dimensions) is required")
    if any(not isinstance(dimension, int) or isinstance(dimension, bool) or dimension <= 0 for dimension in dimensions):
        raise ValueError("matrix dimensions must be positive integers")
    n = len(dimensions) - 1
    dp = [[0] * n for _ in range(n)]
    parent = [[0] * n for _ in range(n)]
    for d in range(2, n + 1):
        for i in range(n - d + 1):
            j = i + d - 1
            best = cost_of_split(dimensions, dp, i, i, j)
            parent[i][j] = i
            for k in range(i + 1, j):
                candidate = cost_of_split(dimensions, dp, i, k, j)
                if candidate < best:
                    best = candidate
                    parent[i][j] = k
            dp[i][j] = best
    return dp[0][-1], parent
