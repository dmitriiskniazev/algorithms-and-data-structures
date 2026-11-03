from data_structures.deque import Deque


class Queue[T]:
    def __init__(self) -> None:
        self.values = Deque[T]()

    def __len__(self) -> int:
        return len(self.values)

    def push(self, value: T) -> None:
        self.values.push_back(value)

    def pop(self) -> T:
        return self.values.pop_front()

    def peek(self) -> T:
        return self.values.front()
