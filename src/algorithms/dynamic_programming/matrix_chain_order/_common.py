from collections.abc import Callable, Sequence

from algorithms.dynamic_programming.matrix_chain_order._types import State, Step


def cost_of_split(dimensions: Sequence[int], dp: Sequence[Sequence[int]], i: int, k: int, j: int) -> int:
    return dp[i][k] + dp[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]


def parenthesize(n: int, split: Callable[[State], Step]) -> str:
    parts: list[str] = []
    stack: list[State | str] = [(0, n - 1)]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            parts.append(item)
            continue
        i, j = item
        if i == j:
            parts.append(f"A{i + 1}")
            continue
        left, right = split(item)
        # Stack order is the reverse of output order: (left*right).
        stack.extend((")", right, "*", left, "("))
    return "".join(parts)
