class Queue[T]:
    def __init__(self) -> None:
        self.incoming: list[T] = []
        self.outgoing: list[T] = []

    def __len__(self) -> int:
        return len(self.incoming) + len(self.outgoing)

    def _transfer(self) -> None:
        if not self.outgoing:
            while self.incoming:
                self.outgoing.append(self.incoming.pop())

    def push(self, value: T) -> None:
        self.incoming.append(value)

    def peek(self) -> T:
        self._transfer()
        if not self.outgoing:
            raise IndexError("empty queue")
        return self.outgoing[-1]

    def pop(self) -> T:
        self.peek()
        return self.outgoing.pop()
