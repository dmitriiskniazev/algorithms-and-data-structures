import random
from collections import deque as reference_deque

import pytest

from data_structures import deque


def test_deque_against_reference():
    actual = deque.Deque()
    expected = reference_deque()
    rng = random.Random(9)
    for index in range(3000):
        action = rng.randrange(4)
        if not expected or action == 0:
            actual.push_front(index)
            expected.appendleft(index)
        elif action == 1:
            actual.push_back(index)
            expected.append(index)
        elif action == 2:
            assert actual.pop_front() == expected.popleft()
        else:
            assert actual.pop_back() == expected.pop()
        assert len(actual) == len(expected)
        if expected:
            assert actual.front() == expected[0]
            assert actual.back() == expected[-1]
    while expected:
        assert actual.pop_back() == expected.pop()
    for method in [actual.front, actual.back, actual.pop_front, actual.pop_back]:
        with pytest.raises(IndexError):
            method()
