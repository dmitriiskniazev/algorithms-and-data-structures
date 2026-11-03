from collections import deque
from collections.abc import Sequence


def restore_from_table(weights: Sequence[int], capacity: int, dp: Sequence[Sequence[int]]) -> list[int]:
    ans: deque[int] = deque()
    c = capacity
    for i in range(len(weights), 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            ans.appendleft(i - 1)
            c -= weights[i - 1]
    return list(ans)
