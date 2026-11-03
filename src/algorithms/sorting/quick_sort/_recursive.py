from collections.abc import MutableSequence
from random import Random

from algorithms.comparable import Comparable
from algorithms.sorting.partition import partition


def recursive[T: Comparable](values: MutableSequence[T], *, rng: Random | None = None) -> None:
    rng = Random() if rng is None else rng
    _sort(values, 0, len(values), rng)


def _sort[T: Comparable](values: MutableSequence[T], left: int, right: int, rng: Random) -> None:
    if right - left < 2:
        return
    equal_left, equal_right = partition(values, left, right, rng.randrange(left, right))
    _sort(values, left, equal_left, rng)
    _sort(values, equal_right, right, rng)
