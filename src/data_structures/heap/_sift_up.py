from collections.abc import MutableSequence

from algorithms.comparable import Comparable


def sift_up[T: Comparable](values: MutableSequence[T], child: int) -> None:
    while child > 0:
        root = (child - 1) // 2
        if not values[root] < values[child]:
            break
        values[root], values[child] = values[child], values[root]
        child = root
