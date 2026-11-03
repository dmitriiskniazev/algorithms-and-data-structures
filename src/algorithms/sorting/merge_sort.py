from collections.abc import MutableSequence

from algorithms.comparable import Comparable


def sort[T: Comparable](values: MutableSequence[T]) -> None:
    buffer = list(values)
    _sort(values, buffer, 0, len(values))


def _sort[T: Comparable](values: MutableSequence[T], buffer: list[T], left: int, right: int) -> None:
    if right - left < 2:
        return
    mid = left + (right - left) // 2
    _sort(values, buffer, left, mid)
    _sort(values, buffer, mid, right)
    _merge(values, buffer, left, mid, right)


def _merge[T: Comparable](values: MutableSequence[T], buffer: list[T], left: int, mid: int, right: int) -> None:
    buffer[left:right] = values[left:right]
    i, j = left, mid
    for k in range(left, right):
        if i == mid:
            values[k] = buffer[j]
            j += 1
        elif j == right or not buffer[j] < buffer[i]:
            values[k] = buffer[i]
            i += 1
        else:
            values[k] = buffer[j]
            j += 1
