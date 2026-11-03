from itertools import product
from algorithms.divide_and_conquer import inversions
from tests.support import Ordered


def test_inversions_against_quadratic_reference() -> None:
    for size in range(7):
        for values in product(range(3), repeat=size):
            expected = sum(values[j] < values[i] for i in range(size) for j in range(i + 1, size))
            assert inversions.count(values) == expected


def test_uses_only_strict_comparison_and_does_not_mutate() -> None:
    values = [Ordered(value) for value in [3, 1, 2, 1]]
    original = [id(value) for value in values]
    assert inversions.count(values) == 4
    assert [id(value) for value in values] == original
