from data_structures.queue.ring import Queue


class Stack[T]:
    def __init__(self) -> None:
        self.active = Queue[T]()
        self.spare = Queue[T]()

    def __len__(self) -> int:
        return len(self.active)

    def push(self, value: T) -> None:
        self.spare.push(value)
        while self.active:
            self.spare.push(self.active.pop())
        self.active, self.spare = self.spare, self.active

    def peek(self) -> T:
        return self.active.peek()

    def pop(self) -> T:
        return self.active.pop()
