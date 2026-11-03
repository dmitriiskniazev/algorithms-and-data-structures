from typing import cast


class Queue[T]:
    def __init__(self) -> None:
        self.values: list[T | None] = [None] * 4
        self.first = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def push(self, value: T) -> None:
        if self._size == len(self.values):
            self.values = [self.values[(self.first + i) % self._size] for i in range(self._size)] + [None] * self._size
            self.first = 0
        self.values[(self.first + self._size) % len(self.values)] = value
        self._size += 1

    def peek(self) -> T:
        if not self._size:
            raise IndexError("empty queue")
        return cast(T, self.values[self.first])

    def pop(self) -> T:
        value = self.peek()
        self.values[self.first] = None
        self.first = (self.first + 1) % len(self.values)
        self._size -= 1
        return value
