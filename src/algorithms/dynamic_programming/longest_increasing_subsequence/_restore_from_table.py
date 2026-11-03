from collections import deque
from collections.abc import Sequence

from algorithms.dynamic_programming.longest_increasing_subsequence._types import State


def restore_from_table(values: Sequence[int], dp: Sequence[int], end: State | None) -> list[int]:
    ans: deque[int] = deque()
    state = end
    while state is not None:
        ans.appendleft(state)
        prev = None
        if dp[state] > 1:
            for j in range(state - 1, -1, -1):
                if dp[j] == dp[state] - 1 and values[j] < values[state]:
                    prev = j
                    break
        state = prev
    return list(ans)
