from algorithms.sorting import insertion_sort


def test_insertion_sort_orders_values_in_place() -> None:
    values = [5, 2, 4, 6, 1, 3]

    result = insertion_sort(values)

    assert values == [1, 2, 3, 4, 5, 6]
    assert result is None


def test_insertion_sort_supports_reverse_and_key() -> None:
    values = ["pear", "fig", "plum", "kiwi"]

    insertion_sort(values, key=len, reverse=True)

    assert values == ["pear", "plum", "kiwi", "fig"]


def test_insertion_sort_is_stable() -> None:
    values = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]

    insertion_sort(values, key=lambda value: value[0])

    assert values == [(1, "b"), (1, "d"), (2, "a"), (2, "c")]


def test_insertion_sort_handles_empty_and_singleton() -> None:
    empty: list[int] = []
    singleton = [1]

    insertion_sort(empty)
    insertion_sort(singleton)

    assert empty == []
    assert singleton == [1]
