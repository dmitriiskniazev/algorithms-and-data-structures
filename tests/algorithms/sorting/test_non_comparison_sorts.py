import random
import pytest
from algorithms.sorting import counting_sort, radix_sort
from tests.support import TaggedInt


@pytest.mark.parametrize("sort", [counting_sort.sort, radix_sort.sort])
def test_integer_sorts_are_stable(sort):
    values = [TaggedInt(value, tag) for value, tag in [(257, "a"), (1, "b"), (257, "c"), (0, "d"), (1, "e")]]
    identities = {id(value) for value in values}
    sort(values)
    assert values == [0, 1, 1, 257, 257]
    assert [value.tag for value in values] == ["d", "b", "e", "a", "c"]
    assert {id(value) for value in values} == identities


@pytest.mark.parametrize("sort", [counting_sort.sort, radix_sort.sort])
def test_random_values_and_byte_boundaries(sort):
    rng = random.Random(25)
    values = [rng.randrange(65537) for _ in range(500)] + [0, 255, 256, 65535, 65536]
    expected = sorted(values)
    sort(values)
    assert values == expected


@pytest.mark.parametrize("sort", [counting_sort.sort, radix_sort.sort])
def test_integer_sorts_validate_before_mutating(sort):
    for invalid in ([-1, 0], [True, 1], [1.5, 2]):
        values = invalid.copy()
        original = values.copy()
        with pytest.raises(ValueError):
            sort(values)
        assert values == original


@pytest.mark.parametrize("sort", [counting_sort.sort, radix_sort.sort])
def test_empty_zero_and_singleton(sort):
    for values in ([], [0], [7]):
        expected = values.copy()
        sort(values)
        assert values == expected
