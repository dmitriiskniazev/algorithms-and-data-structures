from collections.abc import MutableSequence
from random import Random

from algorithms.comparable import Comparable
from algorithms.sorting.partition import partition


def recursive[T: Comparable](values: MutableSequence[T], k: int, *, rng: Random | None = None) -> T:
    if not 0 <= k < len(values):
        raise IndexError("rank outside sequence")
    rng = Random() if rng is None else rng
    return _search(values, k, 0, len(values), rng)


def _search[T: Comparable](values: MutableSequence[T], k: int, left: int, right: int, rng: Random) -> T:
    if right - left < 2:
        return values[k]
    equal_left, equal_right = partition(values, left, right, rng.randrange(left, right))
    if k < equal_left:
        return _search(values, k, left, equal_left, rng)
    if k >= equal_right:
        return _search(values, k, equal_right, right, rng)
    return values[k]
