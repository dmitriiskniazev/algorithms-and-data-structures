from collections.abc import MutableSequence
from random import Random

from algorithms.comparable import Comparable
from algorithms.sorting.partition import partition


def iterative[T: Comparable](values: MutableSequence[T], *, rng: Random | None = None) -> None:
    rng = Random() if rng is None else rng
    stack = [(0, len(values))]
    while stack:
        left, right = stack.pop()
        while right - left > 1:
            equal_left, equal_right = partition(values, left, right, rng.randrange(left, right))
            if equal_left - left < right - equal_right:
                if right - equal_right > 1:
                    stack.append((equal_right, right))
                right = equal_left
            else:
                if equal_left - left > 1:
                    stack.append((left, equal_left))
                left = equal_right
