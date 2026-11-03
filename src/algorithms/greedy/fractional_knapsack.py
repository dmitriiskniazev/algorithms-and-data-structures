from collections.abc import Iterable
from math import isfinite


def solve(items: Iterable[tuple[float, float]], capacity: float) -> float:
    if not isfinite(capacity) or capacity < 0:
        raise ValueError("capacity must be finite and nonnegative")
    items = list(items)
    for weight, value in items:
        if not isfinite(weight) or weight <= 0:
            raise ValueError("item weights must be finite and positive")
        if not isfinite(value) or value < 0:
            raise ValueError("item values must be finite and nonnegative")

    items.sort(key=lambda item: item[1] / item[0], reverse=True)
    val = 0.0
    remaining = capacity
    for weight, value in items:
        amount = min(weight, remaining)
        val += value * (amount / weight)
        remaining -= amount
        if remaining == 0:
            break
    return val
