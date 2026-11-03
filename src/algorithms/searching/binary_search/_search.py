from collections.abc import Sequence

from algorithms.comparable import Comparable

from . import lower_bound


def search[T: Comparable](values: Sequence[T], target: T) -> int | None:
    left = lower_bound.iterative(values, target)
    if left == len(values):
        return None
    if not values[left] < target and not target < values[left]:
        return left
    return None
