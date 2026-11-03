from collections import deque
from collections.abc import Sequence


def restore_from_table(first: str, second: str, dp: Sequence[Sequence[int]]) -> str:
    ans: deque[str] = deque()
    i, j = len(first), len(second)
    while i > 0 and j > 0:
        if first[i - 1] == second[j - 1]:
            ans.appendleft(first[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(ans)
