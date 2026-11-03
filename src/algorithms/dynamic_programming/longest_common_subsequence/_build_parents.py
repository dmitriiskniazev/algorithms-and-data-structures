from algorithms.dynamic_programming.directions import Direction
from algorithms.dynamic_programming.longest_common_subsequence._types import Parents


def build_parents(first: str, second: str) -> tuple[int, Parents]:
    m, n = len(first), len(second)
    parent = [bytearray(n + 1) for _ in range(m + 1)]
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        first_char = first[i - 1]
        curr[0] = 0
        for j in range(1, n + 1):
            second_char = second[j - 1]
            if first_char == second_char:
                curr[j] = prev[j - 1] + 1
                parent[i][j] = Direction.DIAGONAL
            elif prev[j] >= curr[j - 1]:
                curr[j] = prev[j]
                parent[i][j] = Direction.UP
            else:
                curr[j] = curr[j - 1]
                parent[i][j] = Direction.LEFT
        prev, curr = curr, prev
    return prev[-1], parent
