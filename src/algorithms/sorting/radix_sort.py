from collections.abc import MutableSequence

from ._integers import validate


def sort[T: int](values: MutableSequence[T]) -> None:
    validate(values)
    if not values:
        return
    passes = max(1, (max(values).bit_length() + 7) // 8)
    buffer = list(values)
    for shift in range(0, passes * 8, 8):
        _counting_pass(values, buffer, shift)


def _counting_pass[T: int](values: MutableSequence[T], buffer: list[T], shift: int) -> None:
    counts = [0] * 256
    for value in values:
        counts[(value >> shift) & 0xFF] += 1
    for i in range(1, 256):
        counts[i] += counts[i - 1]
    for i in range(len(values) - 1, -1, -1):
        digit = (values[i] >> shift) & 0xFF
        counts[digit] -= 1
        buffer[counts[digit]] = values[i]
    for i, value in enumerate(buffer):
        values[i] = value
