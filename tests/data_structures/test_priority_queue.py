import random
import pytest
from data_structures import priority_queue
from tests.support import Ordered


@pytest.mark.parametrize("variant", ["minimum", "maximum"])
def test_mixed_operations_and_empty(variant):
    actual = getattr(priority_queue, variant).PriorityQueue()
    oracle = []
    rng = random.Random(12)
    for _ in range(1000):
        if oracle and rng.randrange(2) == 0:
            assert actual.pop() == oracle.pop(0 if variant == "minimum" else -1)
        else:
            value = rng.randrange(7)
            actual.push(value)
            oracle.append(value)
            oracle.sort()
        assert len(actual) == len(oracle)
        if oracle:
            assert actual.peek() == oracle[0 if variant == "minimum" else -1]
    while oracle:
        assert actual.pop() == oracle.pop(0 if variant == "minimum" else -1)
    for method in [actual.peek, actual.pop]:
        with pytest.raises(IndexError):
            method()


@pytest.mark.parametrize("variant", ["minimum", "maximum"])
def test_strict_comparison_and_payloads(variant):
    actual = getattr(priority_queue, variant).PriorityQueue()
    values = [Ordered(value, str(i)) for i, value in enumerate([3, 1, 1, 4])]
    for value in values:
        actual.push(value)
    assert actual.peek().value == (1 if variant == "minimum" else 4)
    first = actual.pop()
    assert first.value == (1 if variant == "minimum" else 4)
    extra = Ordered(0, "extra")
    actual.push(extra)
    assert actual.peek().value == (0 if variant == "minimum" else 3)
    remaining = [actual.pop() for _ in range(len(actual))]
    assert {id(value) for value in [first, *remaining]} == {id(value) for value in [*values, extra]}
    assert [value.value for value in remaining] == sorted(
        [value.value for value in [*values, extra] if value is not first], reverse=variant == "maximum"
    )
