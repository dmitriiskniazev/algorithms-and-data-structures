from collections.abc import Sequence


def compute[T](sequence: Sequence[T]) -> list[int]:
    n = len(sequence)
    if n == 0:
        return []
    z = [0] * n
    z[0] = n
    left = right = 0
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < n and sequence[z[i]] == sequence[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z
