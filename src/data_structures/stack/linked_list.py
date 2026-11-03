class _Node[T]:
    def __init__(self, value: T, next: _Node[T] | None) -> None:
        self.value = value
        self.next = next


class Stack[T]:
    def __init__(self) -> None:
        self.first: _Node[T] | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def push(self, value: T) -> None:
        self.first = _Node(value, self.first)
        self._size += 1

    def peek(self) -> T:
        if self.first is None:
            raise IndexError("empty stack")
        return self.first.value

    def pop(self) -> T:
        node = self.first
        if node is None:
            raise IndexError("empty stack")
        self.first = node.next
        self._size -= 1
        return node.value
