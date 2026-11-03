import random
import pytest
from data_structures import queue as queues
from tests.support import Ordered


@pytest.mark.parametrize("variant", ["minimum", "maximum"])
def test_mixed_operations_and_empty(variant):
    actual = getattr(queues.extrema, variant).Queue()
    oracle = []
    rng = random.Random(12)
    for _ in range(1000):
        if oracle and rng.randrange(2) == 0:
            assert actual.pop() == oracle.pop(0)
        else:
            value = rng.randrange(7)
            actual.push(value)
            oracle.append(value)
        assert len(actual) == len(oracle)
        if oracle:
            assert actual.peek() == oracle[0]
            assert actual.extreme() == (min(oracle) if variant == "minimum" else max(oracle))
    while oracle:
        assert actual.pop() == oracle.pop(0)
    for method in [actual.peek, actual.pop, actual.extreme]:
        with pytest.raises(IndexError):
            method()


@pytest.mark.parametrize("variant", ["minimum", "maximum"])
def test_strict_comparison_and_payloads(variant):
    actual = getattr(queues.extrema, variant).Queue()
    values = [Ordered(value, str(i)) for i, value in enumerate([3, 1, 1, 4])]
    for value in values:
        actual.push(value)
    assert actual.extreme().value == (1 if variant == "minimum" else 4)
    first = actual.pop()
    assert first is values[0]
    extra = Ordered(0, "extra")
    actual.push(extra)
    assert actual.extreme().value == (0 if variant == "minimum" else 4)
    remaining = [actual.pop() for _ in range(len(actual))]
    assert {id(value) for value in [first, *remaining]} == {id(value) for value in [*values, extra]}
    assert [value.tag for value in remaining] == ["1", "2", "3", "extra"]
