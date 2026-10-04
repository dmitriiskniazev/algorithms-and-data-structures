from collections.abc import MutableSequence


def swap_at[T](values: MutableSequence[T], i: int, j: int) -> None:
    values[i], values[j] = values[j], values[i]
