from collections.abc import Callable, MutableSequence
from operator import gt, lt

from algorithms.sorting.ordering import prepare_sort_keys
from algorithms.sorting.swap import swap_at


def selection_sort[T, K](
    values: MutableSequence[T], *, key: Callable[[T], K] | None = None, reverse: bool = False
) -> None:
    sort_keys = prepare_sort_keys(values, key)
    comes_before = gt if reverse else lt
    n = len(values)

    for i in range(n):
        minimum = i

        for j in range(i + 1, n):
            candidate = sort_keys[j] if sort_keys is not None else values[j]
            current_minimum = (
                sort_keys[minimum] if sort_keys is not None else values[minimum]
            )

            if comes_before(candidate, current_minimum):
                minimum = j

        if minimum != i:
            swap_at(values, i, minimum)
            if sort_keys is not None:
                swap_at(sort_keys, i, minimum)
