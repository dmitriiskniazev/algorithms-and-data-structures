import random
from dataclasses import FrozenInstanceError

import pytest

from data_structures import stack as stacks


def values(stack):
    result = []
    while stack:
        result.append(stack.peek())
        stack = stack.pop()
    return result


def test_random_branches_preserve_every_version():
    rng = random.Random(37)
    versions = [(stacks.persistent.Stack[int](), [])]
    for i in range(600):
        old, expected = rng.choice(versions)
        if expected and rng.randrange(2):
            new, result = old.pop(), expected[:-1]
        else:
            new, result = old.push(i % 17), [*expected, i % 17]
        versions.append((new, result))
        assert len(old) == len(expected)
        assert values(old) == expected[::-1]
    for stack, expected in versions:
        assert len(stack) == len(expected)
        assert values(stack) == expected[::-1]


def test_shared_tail_and_saved_version_restore():
    empty = stacks.persistent.Stack[object]()
    value = object()
    saved = empty.push(value)
    current = saved.push(None)
    assert current.peek() is None
    assert current.pop().peek() is value
    assert current._first.next is saved._first
    current = saved
    assert current.peek() is value
    assert not empty
    with pytest.raises(FrozenInstanceError):
        saved._size = 100


def test_empty_stack():
    stack = stacks.persistent.Stack[int]()
    with pytest.raises(IndexError):
        stack.peek()
    with pytest.raises(IndexError):
        stack.pop()
    assert not stack


def test_snapshot_undo_and_fork():
    history = [stacks.persistent.Stack[int]()]
    history.append(history[-1].push(10))
    saved = history[-1]
    history.append(history[-1].push(20))

    history.pop()
    current = history[-1]
    assert current.peek() == 10

    left = saved.push(30)
    right = saved.pop()
    assert left.peek() == 30
    assert not right
    assert saved.peek() == 10

    current = saved
    assert current.peek() == 10
