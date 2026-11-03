from collections.abc import MutableSequence

from ._integers import validate


def sort[T: int](values: MutableSequence[T]) -> None:
    validate(values)
    if not values:
        return
    counts = [0] * (max(values) + 1)
    for value in values:
        counts[value] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    buffer = list(values)
    for i in range(len(values) - 1, -1, -1):
        value = values[i]
        counts[value] -= 1
        buffer[counts[value]] = value
    for i, value in enumerate(buffer):
        values[i] = value
