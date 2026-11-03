from collections.abc import Sequence

from algorithms.dynamic_programming.matrix_chain_order._common import cost_of_split, parenthesize
from algorithms.dynamic_programming.matrix_chain_order._types import State, Step


def restore_from_table(dimensions: Sequence[int], dp: Sequence[Sequence[int]]) -> str:
    def find_split(state: State) -> Step:
        i, j = state
        k = next(k for k in range(i, j) if dp[i][j] == cost_of_split(dimensions, dp, i, k, j))
        return (i, k), (k + 1, j)

    return parenthesize(len(dimensions) - 1, find_split)
