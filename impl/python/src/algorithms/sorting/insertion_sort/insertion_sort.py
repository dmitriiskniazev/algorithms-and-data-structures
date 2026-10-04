from collections.abc import Callable, MutableSequence
from operator import gt, lt

from algorithms.sorting.ordering import prepare_sort_keys


def insertion_sort[T, K](
    values: MutableSequence[T], *, key: Callable[[T], K] | None = None, reverse: bool = False
) -> None:
    sort_keys = prepare_sort_keys(values, key)
    comes_before = gt if reverse else lt

    for i in range(1, len(values)):
        value = values[i]
        sort_key = sort_keys[i] if sort_keys is not None else value
        j = i

        while j > 0:
            previous_key = sort_keys[j - 1] if sort_keys is not None else values[j - 1]
            if not comes_before(sort_key, previous_key):
                break

            values[j] = values[j - 1]
            if sort_keys is not None:
                sort_keys[j] = sort_keys[j - 1]
            j -= 1

        values[j] = value
        if sort_keys is not None:
            sort_keys[j] = sort_key
