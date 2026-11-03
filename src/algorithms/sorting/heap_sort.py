from collections.abc import MutableSequence

from algorithms.comparable import Comparable
from data_structures.heap import build, sift_down


def sort[T: Comparable](values: MutableSequence[T]) -> None:
    build(values)
    for right in range(len(values) - 1, 0, -1):
        values[0], values[right] = values[right], values[0]
        sift_down(values, 0, right)
