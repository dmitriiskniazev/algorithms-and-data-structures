from algorithms.sorting import selection_sort


def test_selection_sort_orders_values_in_place() -> None:
    values = [64, 25, 12, 22, 11]

    result = selection_sort(values)

    assert values == [11, 12, 22, 25, 64]
    assert result is None


def test_selection_sort_supports_reverse_and_key() -> None:
    values = ["pear", "fig", "plum", "kiwi"]

    selection_sort(values, key=len, reverse=True)

    assert values == ["pear", "plum", "kiwi", "fig"]


def test_selection_sort_handles_duplicates_and_empty_input() -> None:
    values = [3, 1, 2, 1]
    empty: list[int] = []

    selection_sort(values)
    selection_sort(empty)

    assert values == [1, 1, 2, 3]
    assert empty == []
