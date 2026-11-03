from typing import Protocol

from algorithms.comparable import Comparable

from ._stack import Stack


class ExtremaStack[T: Comparable](Stack[T], Protocol):
    def extreme(self) -> T: ...
