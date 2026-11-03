import random
import pytest
from algorithms.selection import order_statistic
from tests.support import Ordered


@pytest.mark.parametrize("search", [order_statistic.iterative, order_statistic.recursive, order_statistic.by_sorting])
def test_all_ranks(search):
    rng = random.Random(5)
    for size in range(1, 35):
        original = [rng.randrange(-5, 6) for _ in range(size)]
        for k in range(size):
            values = original.copy()
            assert search(values, k) == sorted(original)[k]
            assert sorted(values) == sorted(original)
    for values, k in [([], 0), ([1], -1), ([1], 1)]:
        with pytest.raises(IndexError):
            search(values, k)


@pytest.mark.parametrize("search", [order_statistic.iterative, order_statistic.recursive, order_statistic.by_sorting])
def test_strict_comparison_preserves_records(search):
    values = [Ordered(value) for value in [4, 1, 3, 2]]
    identities = {id(value) for value in values}
    assert search(values, 2).value == 3
    assert {id(value) for value in values} == identities
