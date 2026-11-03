from collections.abc import MutableSequence

from algorithms.comparable import Comparable

from ._sift_down import sift_down


def build[T: Comparable](values: MutableSequence[T]) -> None:
    for root in range(len(values) // 2 - 1, -1, -1):
        sift_down(values, root, len(values))
