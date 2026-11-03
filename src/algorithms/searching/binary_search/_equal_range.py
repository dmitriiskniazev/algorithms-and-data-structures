from collections.abc import Sequence

from algorithms.comparable import Comparable

from . import lower_bound, upper_bound


def equal_range[T: Comparable](values: Sequence[T], target: T) -> tuple[int, int]:
    return lower_bound.iterative(values, target), upper_bound.iterative(values, target)
