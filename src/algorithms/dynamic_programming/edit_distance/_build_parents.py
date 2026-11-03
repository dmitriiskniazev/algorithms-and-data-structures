from algorithms.dynamic_programming.directions import Direction
from algorithms.dynamic_programming.edit_distance._types import Parents


def build_parents(source: str, target: str) -> tuple[int, Parents]:
    m, n = len(source), len(target)
    parent = [bytearray(n + 1) for _ in range(m + 1)]
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    for j in range(1, n + 1):
        parent[0][j] = Direction.LEFT
    for i in range(1, m + 1):
        source_char = source[i - 1]
        curr[0] = i
        parent[i][0] = Direction.UP
        for j in range(1, n + 1):
            target_char = target[j - 1]
            curr[j] = prev[j - 1] + (source_char != target_char)
            direction = Direction.DIAGONAL
            if prev[j] + 1 < curr[j]:
                curr[j] = prev[j] + 1
                direction = Direction.UP
            if curr[j - 1] + 1 < curr[j]:
                curr[j] = curr[j - 1] + 1
                direction = Direction.LEFT
            parent[i][j] = direction
        prev, curr = curr, prev
    return prev[-1], parent
