from collections.abc import Sequence

from algorithms.comparable import Comparable


def count[T: Comparable](values: Sequence[T]) -> int:
    order = list(values)
    buffer = order.copy()
    return _sort_and_count(order, buffer, 0, len(order))


def _sort_and_count[T: Comparable](values: list[T], buffer: list[T], left: int, right: int) -> int:
    if right - left < 2:
        return 0
    mid = left + (right - left) // 2
    count = _sort_and_count(values, buffer, left, mid) + _sort_and_count(values, buffer, mid, right)
    return count + _merge_and_count(values, buffer, left, mid, right)


def _merge_and_count[T: Comparable](values: list[T], buffer: list[T], left: int, mid: int, right: int) -> int:
    buffer[left:right] = values[left:right]
    i, j, k = left, mid, left
    count = 0
    while i < mid and j < right:
        if buffer[j] < buffer[i]:
            values[k] = buffer[j]
            count += mid - i
            j += 1
        else:
            values[k] = buffer[i]
            i += 1
        k += 1
    while i < mid:
        values[k] = buffer[i]
        i += 1
        k += 1
    while j < right:
        values[k] = buffer[j]
        j += 1
        k += 1
    return count
