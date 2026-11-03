class _Node[T]:
    def __init__(self, value: T) -> None:
        self.value = value
        self.prev: _Node[T] | None = None
        self.next: _Node[T] | None = None


class Deque[T]:
    def __init__(self) -> None:
        self.first: _Node[T] | None = None
        self.last: _Node[T] | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def push_front(self, value: T) -> None:
        node = _Node(value)
        node.next = self.first
        if self.first is None:
            self.last = node
        else:
            self.first.prev = node
        self.first = node
        self._size += 1

    def push_back(self, value: T) -> None:
        node = _Node(value)
        node.prev = self.last
        if self.last is None:
            self.first = node
        else:
            self.last.next = node
        self.last = node
        self._size += 1

    def front(self) -> T:
        if self.first is None:
            raise IndexError("empty deque")
        return self.first.value

    def back(self) -> T:
        if self.last is None:
            raise IndexError("empty deque")
        return self.last.value

    def pop_front(self) -> T:
        node = self.first
        if node is None:
            raise IndexError("empty deque")
        self.first = node.next
        node.next = None
        if self.first is None:
            self.last = None
        else:
            self.first.prev = None
        self._size -= 1
        return node.value

    def pop_back(self) -> T:
        node = self.last
        if node is None:
            raise IndexError("empty deque")
        self.last = node.prev
        node.prev = None
        if self.last is None:
            self.first = None
        else:
            self.last.next = None
        self._size -= 1
        return node.value
