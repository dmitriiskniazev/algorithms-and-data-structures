from collections.abc import MutableSequence

from algorithms.comparable import Comparable


def sort[T: Comparable](values: MutableSequence[T]) -> None:
    for i in range(1, len(values)):
        _insert(values, i)


def _insert[T: Comparable](values: MutableSequence[T], i: int) -> None:
    value = values[i]
    while i > 0 and value < values[i - 1]:
        values[i] = values[i - 1]
        i -= 1
    values[i] = value
