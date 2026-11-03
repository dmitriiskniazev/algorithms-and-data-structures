from collections import deque
from collections.abc import Sequence

from algorithms.dynamic_programming.edit_distance._types import Edit, EditKind


def restore_from_table(source: str, target: str, dp: Sequence[Sequence[int]]) -> list[Edit]:
    ans: deque[Edit] = deque()
    i, j = len(source), len(target)
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (source[i - 1] != target[j - 1]):
            kind: EditKind = "match" if source[i - 1] == target[j - 1] else "replace"
            ans.appendleft(Edit(kind, source[i - 1], target[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ans.appendleft(Edit("delete", source[i - 1], None))
            i -= 1
        else:
            ans.appendleft(Edit("insert", None, target[j - 1]))
            j -= 1
    return list(ans)
