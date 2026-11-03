import random

from algorithms.sorting import merge_sort
from tests.support import Ordered


def test_sort_against_reference() -> None:
    rng = random.Random(14)
    for size in range(80):
        values = [rng.randrange(-9, 10) for _ in range(size)]
        expected = sorted(values)
        assert merge_sort.sort(values) is None
        assert values == expected
    words = ["pear", "fig", "plum", "kiwi"]
    merge_sort.sort(words)
    assert words == ["fig", "kiwi", "pear", "plum"]


def test_sort_uses_only_strict_comparison_and_preserves_payloads() -> None:
    values = [Ordered(value, tag) for value, tag in [(2, "a"), (1, "b"), (2, "c"), (1, "d")]]
    identities = {id(value) for value in values}
    merge_sort.sort(values)
    assert [value.value for value in values] == [1, 1, 2, 2]
    assert {id(value) for value in values} == identities
    assert [value.tag for value in values] == ["b", "d", "a", "c"]
