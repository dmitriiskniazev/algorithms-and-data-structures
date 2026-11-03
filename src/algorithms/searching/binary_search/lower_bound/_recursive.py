from collections.abc import Sequence

from algorithms.comparable import Comparable


def recursive[T: Comparable](values: Sequence[T], target: T) -> int:
    return _search(values, target, 0, len(values))


def _search[T: Comparable](values: Sequence[T], target: T, left: int, right: int) -> int:
    if left == right:
        return left
    mid = left + (right - left) // 2
    if values[mid] < target:
        return _search(values, target, mid + 1, right)
    return _search(values, target, left, mid)
