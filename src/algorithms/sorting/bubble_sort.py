from collections.abc import MutableSequence

from algorithms.comparable import Comparable


def sort[T: Comparable](values: MutableSequence[T]) -> None:
    right = len(values)
    while right > 1:
        right = _pass(values, right)


def _pass[T: Comparable](values: MutableSequence[T], right: int) -> int:
    last_swap = 0
    for i in range(1, right):
        if values[i] < values[i - 1]:
            values[i - 1], values[i] = values[i], values[i - 1]
            last_swap = i
    return last_swap
