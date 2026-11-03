from collections.abc import MutableSequence
from random import Random

from algorithms.comparable import Comparable
from algorithms.selection._select_rank import select_rank


def find[T: Comparable](values: MutableSequence[T], *, rng: Random | None = None) -> tuple[T, T]:
    if not values:
        raise IndexError("median of empty sequence")
    rng = Random() if rng is None else rng
    n = len(values)
    lower = select_rank(values, (n - 1) // 2, rng)
    upper = lower if n % 2 else select_rank(values, n // 2, rng)
    return lower, upper
