from collections.abc import Sequence

from algorithms.dynamic_programming.knapsack_01._types import Parents


def build_parents(weights: Sequence[int], values: Sequence[int], capacity: int) -> tuple[int, Parents]:
    n = len(weights)
    parent = [bytearray(capacity + 1) for _ in range(n + 1)]
    prev = [0] * (capacity + 1)
    curr = [0] * (capacity + 1)
    for i in range(1, n + 1):
        weight, value = weights[i - 1], values[i - 1]
        for c in range(capacity + 1):
            curr[c] = prev[c]
            if weight <= c:
                candidate = prev[c - weight] + value
                if candidate > curr[c]:
                    curr[c] = candidate
                    parent[i][c] = 1
        prev, curr = curr, prev
    return prev[capacity], parent
