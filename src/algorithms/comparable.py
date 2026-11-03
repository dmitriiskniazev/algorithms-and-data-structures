from typing import Protocol, Self


class Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...
