from collections.abc import MutableSequence
from random import Random

from algorithms.comparable import Comparable
from algorithms.sorting.partition import partition


def select_rank[T: Comparable](values: MutableSequence[T], k: int, rng: Random) -> T:
    left, right = 0, len(values)
    while right - left > 1:
        equal_left, equal_right = partition(values, left, right, rng.randrange(left, right))
        if k < equal_left:
            right = equal_left
        elif k >= equal_right:
            left = equal_right
        else:
            break
    return values[k]
