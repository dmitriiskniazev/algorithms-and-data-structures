import random

import pytest

from data_structures import stack as stacks


@pytest.mark.parametrize(
    "kind", [stacks.dynamic_array.Stack, stacks.linked_list.Stack, stacks.one_queue.Stack, stacks.two_queues.Stack]
)
def test_stack_against_list(kind):
    stack = kind()
    expected = []
    rng = random.Random(5)
    for index in range(1000):
        if expected and rng.randrange(3) == 0:
            assert stack.peek() == expected[-1]
            assert stack.pop() == expected.pop()
        else:
            value = rng.randrange(100)
            stack.push(value)
            expected.append(value)
        assert len(stack) == len(expected)
    while expected:
        assert stack.pop() == expected.pop()
    for method in [stack.pop, stack.peek]:
        with pytest.raises(IndexError):
            method()
    stack.push(None)
    assert stack.pop() is None
