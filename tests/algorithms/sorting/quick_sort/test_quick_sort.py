import random
import pytest
from algorithms.sorting import quick_sort
from tests.support import Ordered


@pytest.mark.parametrize("sort", [quick_sort.iterative, quick_sort.recursive])
def test_quicksort_against_reference(sort):
    rng = random.Random(14)
    for size in range(80):
        values = [rng.randrange(-9, 10) for _ in range(size)]
        expected = sorted(values)
        sort(values, rng=random.Random(8))
        assert values == expected


@pytest.mark.parametrize("sort", [quick_sort.iterative, quick_sort.recursive])
def test_strict_comparison_and_payloads(sort):
    values = [Ordered(i % 5, str(i)) for i in range(30)]
    identities = {id(value) for value in values}
    sort(values, rng=random.Random(2))
    assert [value.value for value in values] == sorted(i % 5 for i in range(30))
    assert {id(value) for value in values} == identities


@pytest.mark.parametrize("sort", [quick_sort.iterative, quick_sort.recursive])
def test_all_equivalent_values(sort):
    values = [1] * 10000
    sort(values, rng=random.Random(4))
    assert values == [1] * 10000
