from collections.abc import MutableSequence

from algorithms.comparable import Comparable
from algorithms.sorting import heap_sort


def by_sorting[T: Comparable](values: MutableSequence[T], k: int) -> T:
    if not 0 <= k < len(values):
        raise IndexError("rank outside sequence")
    heap_sort.sort(values)
    return values[k]
