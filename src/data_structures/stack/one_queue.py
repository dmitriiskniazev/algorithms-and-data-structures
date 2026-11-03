from data_structures.queue.ring import Queue


class Stack[T]:
    def __init__(self) -> None:
        self.values = Queue[T]()

    def __len__(self) -> int:
        return len(self.values)

    def push(self, value: T) -> None:
        self.values.push(value)
        for _ in range(len(self.values) - 1):
            self.values.push(self.values.pop())

    def peek(self) -> T:
        return self.values.peek()

    def pop(self) -> T:
        return self.values.pop()
