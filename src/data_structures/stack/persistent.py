from dataclasses import dataclass


@dataclass(frozen=True, slots=True, eq=False)
class _Node[T]:
    value: T
    next: _Node[T] | None


@dataclass(frozen=True, slots=True, eq=False)
class Stack[T]:
    _first: _Node[T] | None = None
    _size: int = 0

    def __len__(self) -> int:
        return self._size

    def push(self, value: T) -> Stack[T]:
        return Stack(_Node(value, self._first), self._size + 1)

    def peek(self) -> T:
        if self._first is None:
            raise IndexError("empty stack")
        return self._first.value

    def pop(self) -> Stack[T]:
        if self._first is None:
            raise IndexError("empty stack")
        return Stack(self._first.next, self._size - 1)
