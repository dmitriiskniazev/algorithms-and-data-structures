from collections.abc import Sequence


def validate(values: Sequence[int]) -> None:
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
        raise ValueError("sorting requires nonnegative integers")
