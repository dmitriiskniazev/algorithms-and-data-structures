from collections.abc import MutableSequence

from algorithms.comparable import Comparable


def sort[T: Comparable](values: MutableSequence[T]) -> None:
    n = len(values)
    for i in range(n):
        best = _minimum_index(values, i, n)
        if best != i:
            values[i], values[best] = values[best], values[i]


def _minimum_index[T: Comparable](values: MutableSequence[T], left: int, right: int) -> int:
    best = left
    for i in range(left + 1, right):
        if values[i] < values[best]:
            best = i
    return best
