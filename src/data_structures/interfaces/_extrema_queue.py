from typing import Protocol

from algorithms.comparable import Comparable

from ._queue import Queue


class ExtremaQueue[T: Comparable](Queue[T], Protocol):
    def extreme(self) -> T: ...
