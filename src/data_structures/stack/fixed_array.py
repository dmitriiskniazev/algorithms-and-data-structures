from typing import cast


class Stack[T]:
    def __init__(self, capacity: int) -> None:
        self.values: list[T | None] = [None] * capacity
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def capacity(self) -> int:
        return len(self.values)

    def push(self, value: T) -> None:
        if self._size == len(self.values):
            raise OverflowError("full stack")
        self.values[self._size] = value
        self._size += 1

    def peek(self) -> T:
        if not self._size:
            raise IndexError("empty stack")
        return cast(T, self.values[self._size - 1])

    def pop(self) -> T:
        value = self.peek()
        self._size -= 1
        self.values[self._size] = None
        return value
