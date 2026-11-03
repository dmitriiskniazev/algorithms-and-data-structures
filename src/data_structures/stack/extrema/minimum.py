from algorithms.comparable import Comparable

from ._types import Entry


class Stack[T: Comparable]:
    def __init__(self) -> None:
        self.values: list[Entry[T]] = []

    def __len__(self) -> int:
        return len(self.values)

    def push(self, value: T) -> None:
        extreme = value
        if self.values and not value < self.values[-1].extreme:
            extreme = self.values[-1].extreme
        self.values.append(Entry(value, extreme))

    def _peek_entry(self) -> Entry[T]:
        if not self.values:
            raise IndexError("empty extrema stack")
        return self.values[-1]

    def peek(self) -> T:
        return self._peek_entry().value

    def pop(self) -> T:
        self._peek_entry()
        return self.values.pop().value

    def extreme(self) -> T:
        return self._peek_entry().extreme
