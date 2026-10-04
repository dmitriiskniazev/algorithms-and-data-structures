from algorithms.sorting import bubble_sort


def test_bubble_sort_orders_values_in_place() -> None:
    values = [5, 1, 4, 2, 8]

    result = bubble_sort(values)

    assert values == [1, 2, 4, 5, 8]
    assert result is None


def test_bubble_sort_supports_reverse_and_key() -> None:
    values = ["pear", "fig", "plum", "kiwi"]
    calls: list[str] = []

    bubble_sort(values, key=lambda value: calls.append(value) or len(value), reverse=True)

    assert values == ["pear", "plum", "kiwi", "fig"]
    assert calls == ["pear", "fig", "plum", "kiwi"]


def test_bubble_sort_is_stable() -> None:
    values = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]

    bubble_sort(values, key=lambda value: value[0])

    assert values == [(1, "b"), (1, "d"), (2, "a"), (2, "c")]


def test_bubble_sort_handles_empty_and_singleton() -> None:
    empty: list[int] = []
    singleton = [1]

    bubble_sort(empty)
    bubble_sort(singleton)

    assert empty == []
    assert singleton == [1]
