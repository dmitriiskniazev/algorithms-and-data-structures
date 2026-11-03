from bisect import bisect_left, bisect_right
from itertools import combinations_with_replacement
from typing import Self

import pytest

from algorithms.searching import binary_search


@pytest.mark.parametrize("variant", ["iterative", "recursive"])
def test_bounds_match_bisect_on_all_small_sorted_sequences(variant: str) -> None:
    lower = getattr(binary_search.lower_bound, variant)
    upper = getattr(binary_search.upper_bound, variant)
    for n in range(7):
        for values in combinations_with_replacement(range(-2, 3), n):
            for target in range(-3, 4):
                left, right = bisect_left(values, target), bisect_right(values, target)
                assert lower(values, target) == left
                assert upper(values, target) == right
                assert binary_search.equal_range(values, target) == (left, right)
                assert binary_search.search(values, target) == (left if left < right else None)


class Ordered:
    def __init__(self, value: int) -> None:
        self.value = value

    def __lt__(self, other: Self, /) -> bool:
        return self.value < other.value

    def __eq__(self, other: object, /) -> bool:
        raise AssertionError("Search must use order equivalence, not equality")


@pytest.mark.parametrize("variant", ["iterative", "recursive"])
def test_only_strict_comparison_is_required(variant: str) -> None:
    lower = getattr(binary_search.lower_bound, variant)
    upper = getattr(binary_search.upper_bound, variant)
    values = [Ordered(value) for value in [1, 2, 2, 2, 5]]
    assert lower(values, Ordered(2)) == 1
    assert upper(values, Ordered(2)) == 4
    assert binary_search.equal_range(values, Ordered(2)) == (1, 4)
    assert binary_search.search(values, Ordered(2)) == 1
    assert binary_search.search(values, Ordered(4)) is None


@pytest.mark.parametrize(
    "operation",
    [
        "lower_bound.iterative",
        "lower_bound.recursive",
        "upper_bound.iterative",
        "upper_bound.recursive",
        "equal_range",
        "search",
    ],
)
@pytest.mark.parametrize("n", [0, 1, 2**30])
def test_access_remains_logarithmic_without_materializing_input(operation: str, n: int) -> None:
    target = n // 2
    if "." in operation:
        name, variant = operation.split(".")
        function = getattr(getattr(binary_search, name), variant)
    else:
        name = operation
        function = getattr(binary_search, name)
    result = function(range(n), target)
    if name == "lower_bound":
        assert result == target
    elif name == "upper_bound":
        assert result == (target + 1 if n else 0)
    elif name == "equal_range":
        assert result == (target, target + 1 if n else 0)
    else:
        assert result == (target if n else None)


def test_binary_search_returns_first_duplicate_and_handles_absence() -> None:
    assert binary_search.search([], 2) is None
    assert binary_search.search([1, 2, 2, 2, 5], 2) == 1
    assert binary_search.search([1, 2, 2, 2, 5], 4) is None


@pytest.mark.parametrize("variant", ["iterative", "recursive"])
def test_comparisons_are_logarithmic(variant):
    calls = []

    class Counted(Ordered):
        def __lt__(self, other: Self, /) -> bool:
            calls.append(1)
            return self.value < other.value

    values = [Counted(i) for i in range(1024)]
    original = [id(value) for value in values]
    for operation in [binary_search.lower_bound, binary_search.upper_bound]:
        calls.clear()
        getattr(operation, variant)(values, Counted(512))
        assert len(calls) <= len(values).bit_length()
    assert [id(value) for value in values] == original
