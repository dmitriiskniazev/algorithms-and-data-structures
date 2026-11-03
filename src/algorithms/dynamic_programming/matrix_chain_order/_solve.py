from collections.abc import Sequence

from algorithms.dynamic_programming.matrix_chain_order._build_table import build_table
from algorithms.dynamic_programming.matrix_chain_order._restore_from_table import restore_from_table


def solve(dimensions: Sequence[int]) -> tuple[int, str]:
    dp = build_table(dimensions)
    return dp[0][-1], restore_from_table(dimensions, dp)
