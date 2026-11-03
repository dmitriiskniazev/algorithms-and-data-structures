from collections.abc import MutableSequence
from random import Random

from algorithms.comparable import Comparable
from algorithms.selection._select_rank import select_rank


def iterative[T: Comparable](values: MutableSequence[T], k: int, *, rng: Random | None = None) -> T:
    if not 0 <= k < len(values):
        raise IndexError("rank outside sequence")
    rng = Random() if rng is None else rng
    return select_rank(values, k, rng)
