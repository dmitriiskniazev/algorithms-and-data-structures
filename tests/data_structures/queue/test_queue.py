import random
from collections import deque

import pytest

from data_structures import queue as queues


@pytest.mark.parametrize("kind", [queues.linked_list.Queue, queues.ring.Queue, queues.two_stacks.Queue])
def test_queue_against_deque(kind):
    queue = kind()
    expected = deque()
    rng = random.Random(2)
    for index in range(3000):
        if expected and rng.randrange(2) == 0:
            assert queue.peek() == expected[0]
            assert queue.pop() == expected.popleft()
        else:
            queue.push(index)
            expected.append(index)
        assert len(queue) == len(expected)
    while expected:
        assert queue.pop() == expected.popleft()
    for method in [queue.pop, queue.peek]:
        with pytest.raises(IndexError):
            method()
    queue.push(None)
    assert queue.pop() is None
