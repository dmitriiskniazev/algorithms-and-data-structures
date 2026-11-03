from collections.abc import Sequence

from algorithms.dynamic_programming.directions import Direction
from algorithms.dynamic_programming.edit_distance._types import Edit, EditKind


def restore_from_parents(source: str, target: str, parent: Sequence[Sequence[int]]) -> list[Edit]:
    ans: list[Edit] = []
    i, j = len(source), len(target)
    while i > 0 or j > 0:
        direction = parent[i][j]
        if direction == Direction.DIAGONAL:
            kind: EditKind = "match" if source[i - 1] == target[j - 1] else "replace"
            ans.append(Edit(kind, source[i - 1], target[j - 1]))
            i -= 1
            j -= 1
        elif direction == Direction.UP:
            ans.append(Edit("delete", source[i - 1], None))
            i -= 1
        else:
            ans.append(Edit("insert", None, target[j - 1]))
            j -= 1
    ans.reverse()
    return ans
