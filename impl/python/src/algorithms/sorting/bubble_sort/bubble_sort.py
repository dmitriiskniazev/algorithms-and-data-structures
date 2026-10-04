from collections.abc import Callable, MutableSequence
from operator import gt, lt

from algorithms.sorting.ordering import prepare_sort_keys
from algorithms.sorting.swap import swap_at


def bubble_sort[T, K](
    values: MutableSequence[T], *, key: Callable[[T], K] | None = None, reverse: bool = False
) -> None:
    sort_keys = prepare_sort_keys(values, key)
    comes_before = gt if reverse else lt
    n = len(values)

    while n > 1:
        last_swap = 0

        for i in range(1, n):
            left = sort_keys[i - 1] if sort_keys is not None else values[i - 1]
            right = sort_keys[i] if sort_keys is not None else values[i]

            if comes_before(right, left):
                swap_at(values, i - 1, i)
                if sort_keys is not None:
                    swap_at(sort_keys, i - 1, i)
                last_swap = i

        if last_swap == 0:
            break

        n = last_swap
