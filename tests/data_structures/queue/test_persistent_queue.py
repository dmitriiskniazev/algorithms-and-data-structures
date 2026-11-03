import random

import pytest

from data_structures import queue as queues


def values(queue):
    result = []
    while queue:
        result.append(queue.peek())
        queue = queue.pop()
    return result


def test_random_branches_preserve_every_version():
    rng = random.Random(41)
    versions = [(queues.persistent.Queue[int](), [])]
    for i in range(600):
        old, expected = rng.choice(versions)
        if expected and rng.randrange(2):
            new, result = old.pop(), expected[1:]
        else:
            new, result = old.push(i % 17), [*expected, i % 17]
        versions.append((new, result))
        assert len(old) == len(expected)
        assert values(old) == expected
    for queue, expected in versions:
        assert len(queue) == len(expected)
        assert values(queue) == expected


def test_transfer_repeats_safely_on_independent_branches():
    saved = queues.persistent.Queue[int]()
    for i in range(64):
        saved = saved.push(i)
    branches = [saved.pop() for _ in range(12)]
    for i, branch in enumerate(branches):
        assert values(branch.push(100 + i)) == [*range(1, 64), 100 + i]
        assert values(branch) == list(range(1, 64))
    assert values(saved) == list(range(64))
    current = saved.pop().push(64)
    assert values(current) == list(range(1, 65))
    current = saved
    assert current.peek() == 0


def test_repeated_reads_and_empty_versions():
    empty = queues.persistent.Queue[object]()
    with pytest.raises(IndexError):
        empty.peek()
    with pytest.raises(IndexError):
        empty.pop()
    value = object()
    queue = empty.push(value).push(None)
    for _ in range(10):
        assert queue.peek() is value
    tail = queue.pop()
    assert tail.peek() is None
    assert not tail.pop()
    assert len(queue) == 2
    assert not empty
