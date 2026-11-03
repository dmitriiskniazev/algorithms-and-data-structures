import random
import weakref

import pytest

from data_structures import stack as stacks


@pytest.mark.parametrize("capacity", [0, 1, 7, 32])
def test_fixed_capacity_against_list(capacity):
    stack = stacks.fixed_array.Stack[int](capacity)
    expected = []
    rng = random.Random(31)
    for i in range(500):
        if expected and rng.randrange(3) == 0:
            assert stack.peek() == expected[-1]
            assert stack.pop() == expected.pop()
        elif len(expected) == capacity:
            with pytest.raises(OverflowError):
                stack.push(i)
        else:
            stack.push(i)
            expected.append(i)
        assert len(stack) == len(expected)
        assert stack.capacity() == capacity
    while expected:
        assert stack.pop() == expected.pop()
    with pytest.raises(IndexError):
        stack.pop()
    with pytest.raises(IndexError):
        stack.peek()


def test_removed_values_are_released_and_none_is_a_value():
    class Value:
        pass

    stack = stacks.fixed_array.Stack[Value | None](1)
    value = Value()
    ref = weakref.ref(value)
    stack.push(value)
    del value
    value = stack.pop()
    assert ref() is value
    del value
    assert ref() is None
    stack.push(None)
    assert stack.peek() is None
    assert stack.pop() is None
