from collections.abc import Sequence

from algorithms.complexity._common import _is_nonnegative_int


def verify(weights: Sequence[int], target: int, certificate: Sequence[int]) -> bool:
    if not _is_nonnegative_int(target) or any(not _is_nonnegative_int(weight) for weight in weights):
        return False
    try:
        indices = tuple(certificate)
    except TypeError:
        return False
    if any(not _is_nonnegative_int(i) or i >= len(weights) for i in indices):
        return False
    if len(set(indices)) != len(indices):
        return False
    return sum(weights[i] for i in indices) == target
