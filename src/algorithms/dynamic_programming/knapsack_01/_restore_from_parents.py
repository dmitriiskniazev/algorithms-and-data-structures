from collections.abc import Sequence


def restore_from_parents(weights: Sequence[int], capacity: int, parent: Sequence[Sequence[int]]) -> list[int]:
    ans: list[int] = []
    c = capacity
    for i in range(len(weights), 0, -1):
        if parent[i][c]:
            ans.append(i - 1)
            c -= weights[i - 1]
    ans.reverse()
    return ans
