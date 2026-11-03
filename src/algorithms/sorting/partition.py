from collections.abc import MutableSequence

from algorithms.comparable import Comparable


def partition[T: Comparable](values: MutableSequence[T], left: int, right: int, pivot: int) -> tuple[int, int]:
    pivot_value = values[pivot]
    equal_left = i = left
    equal_right = right
    while i < equal_right:
        if values[i] < pivot_value:
            values[equal_left], values[i] = values[i], values[equal_left]
            equal_left += 1
            i += 1
        elif pivot_value < values[i]:
            equal_right -= 1
            values[i], values[equal_right] = values[equal_right], values[i]
        else:
            i += 1
    return equal_left, equal_right
