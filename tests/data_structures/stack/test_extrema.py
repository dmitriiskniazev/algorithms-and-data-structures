import random

import pytest

from data_structures.stack import extrema
from tests.support import Ordered


@pytest.mark.parametrize("variant", ["minimum", "maximum"])
def test_mixed_operations_and_empty(variant):
    stack = getattr(extrema, variant).Stack[int]()
    oracle = []
    rng = random.Random(12)
    for _ in range(1000):
        if oracle and rng.randrange(2) == 0:
            assert stack.pop() == oracle.pop()
        else:
            value = rng.randrange(7)
            stack.push(value)
            oracle.append(value)
        assert len(stack) == len(oracle)
        if oracle:
            assert stack.peek() == oracle[-1]
            assert stack.extreme() == (min(oracle) if variant == "minimum" else max(oracle))
    while oracle:
        assert stack.pop() == oracle.pop()
    for method in [stack.pop, stack.peek, stack.extreme]:
        with pytest.raises(IndexError):
            method()


@pytest.mark.parametrize("variant", ["minimum", "maximum"])
def test_strict_comparison_and_duplicate_extrema(variant):
    stack = getattr(extrema, variant).Stack[Ordered]()
    values = [Ordered(value, str(i)) for i, value in enumerate([3, 1, 1, 4])]
    for value in values:
        stack.push(value)
    assert stack.extreme().value == (1 if variant == "minimum" else 4)
    assert stack.pop() is values[-1]
    assert stack.extreme().value == (1 if variant == "minimum" else 3)
    assert stack.pop() is values[-2]
    assert stack.extreme().value == (1 if variant == "minimum" else 3)
    assert stack.pop() is values[-3]
    assert stack.extreme() is values[0]
