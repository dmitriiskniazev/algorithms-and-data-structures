from collections import deque
from collections.abc import Sequence

from algorithms.dynamic_programming.directions import Direction


def restore_from_parents(first: str, second: str, parent: Sequence[Sequence[int]]) -> str:
    ans: deque[str] = deque()
    i, j = len(first), len(second)
    while i > 0 and j > 0:
        direction = parent[i][j]
        if direction == Direction.DIAGONAL:
            ans.appendleft(first[i - 1])
            i -= 1
            j -= 1
        elif direction == Direction.UP:
            i -= 1
        else:
            j -= 1
    return "".join(ans)
