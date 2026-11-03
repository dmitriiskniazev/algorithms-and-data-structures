import random
import pytest
from algorithms.selection import median
from tests.support import Ordered


def test_pair_of_central_elements():
    rng = random.Random(6)
    for size in range(1, 80):
        values = [rng.randrange(10) for _ in range(size)]
        expected = sorted(values)
        assert median.find(values, rng=rng) == (expected[(size - 1) // 2], expected[size // 2])
    with pytest.raises(IndexError):
        median.find([])


def test_strict_comparison_and_record_identity():
    values = [Ordered(value) for value in [8, 1, 7, 2]]
    lower, upper = median.find(values)
    assert (lower.value, upper.value) == (2, 7)
    assert any(lower is value for value in values)
    assert any(upper is value for value in values)


def test_odd_median_repeats_same_record():
    values = [Ordered(value) for value in [0, 1, 1]]
    lower, upper = median.find(values, rng=random.Random(2))
    assert lower is upper
    assert lower.value == 1
