from collections.abc import Sequence

from algorithms.comparable import Comparable


def iterative[T: Comparable](values: Sequence[T], target: T) -> int:
    left, right = 0, len(values)
    while left < right:
        mid = left + (right - left) // 2
        if target < values[mid]:
            right = mid
        else:
            left = mid + 1
    return left
