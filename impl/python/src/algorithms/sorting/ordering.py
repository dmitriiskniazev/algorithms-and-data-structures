from collections.abc import Callable, MutableSequence


def prepare_sort_keys[T, K](
    values: MutableSequence[T], key: Callable[[T], K] | None
) -> list[K] | None:
    if key is None:
        return None

    return [key(value) for value in values]
