from collections.abc import Sequence

from algorithms.comparable import Comparable


def iterative[T: Comparable](values: Sequence[T], target: T) -> int:
    left, right = 0, len(values)
    while left < right:
        mid = left + (right - left) // 2
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
