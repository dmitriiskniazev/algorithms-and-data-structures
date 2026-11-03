from algorithms.comparable import Comparable
from data_structures.stack.extrema.minimum import Stack


class Queue[T: Comparable]:
    def __init__(self) -> None:
        self.incoming = Stack[T]()
        self.outgoing = Stack[T]()

    def __len__(self) -> int:
        return len(self.incoming) + len(self.outgoing)

    def push(self, value: T) -> None:
        self.incoming.push(value)

    def _transfer(self) -> None:
        if not self.outgoing:
            while self.incoming:
                self.outgoing.push(self.incoming.pop())

    def peek(self) -> T:
        self._transfer()
        return self.outgoing.peek()

    def pop(self) -> T:
        self._transfer()
        return self.outgoing.pop()

    def extreme(self) -> T:
        if not self.incoming:
            return self.outgoing.extreme()
        if not self.outgoing:
            return self.incoming.extreme()
        left, right = self.incoming.extreme(), self.outgoing.extreme()
        return left if left < right else right
