from typing import Protocol

from algorithms.comparable import Comparable

from ._queue import Queue


class PriorityQueue[T: Comparable](Queue[T], Protocol):
    pass
