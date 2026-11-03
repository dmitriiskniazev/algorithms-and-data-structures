from collections import deque
from collections.abc import Sequence

from algorithms.dynamic_programming.longest_increasing_subsequence._types import State


def restore_from_parents(end: State | None, parent: Sequence[State | None]) -> list[int]:
    ans: deque[int] = deque()
    state = end
    while state is not None:
        ans.appendleft(state)
        state = parent[state]
    return list(ans)
