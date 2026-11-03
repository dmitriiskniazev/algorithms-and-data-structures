from collections.abc import MutableSequence

from algorithms.comparable import Comparable


def sift_down[T: Comparable](values: MutableSequence[T], root: int, right: int) -> None:
    while 2 * root + 1 < right:
        child = 2 * root + 1
        if child + 1 < right and values[child] < values[child + 1]:
            child += 1
        if not values[root] < values[child]:
            break
        values[root], values[child] = values[child], values[root]
        root = child
