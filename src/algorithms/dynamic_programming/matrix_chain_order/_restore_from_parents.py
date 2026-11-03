from collections.abc import Sequence

from algorithms.dynamic_programming.matrix_chain_order._common import parenthesize
from algorithms.dynamic_programming.matrix_chain_order._types import State, Step


def restore_from_parents(dimensions: Sequence[int], parent: Sequence[Sequence[int]]) -> str:
    def split(state: State) -> Step:
        i, j = state
        k = parent[i][j]
        return (i, k), (k + 1, j)

    return parenthesize(len(dimensions) - 1, split)
