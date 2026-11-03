from dataclasses import dataclass, field

from data_structures.stack.persistent import Stack


@dataclass(frozen=True, slots=True, eq=False)
class Queue[T]:
    _front: Stack[T] = field(default_factory=lambda: Stack[T]())
    _rear: Stack[T] = field(default_factory=lambda: Stack[T]())

    def __len__(self) -> int:
        return len(self._front) + len(self._rear)

    def push(self, value: T) -> Queue[T]:
        if not self._front:
            return Queue(self._front.push(value), self._rear)
        return Queue(self._front, self._rear.push(value))

    def peek(self) -> T:
        if not self._front:
            raise IndexError("empty queue")
        return self._front.peek()

    def pop(self) -> Queue[T]:
        self.peek()
        front, rear = self._front.pop(), self._rear
        if not front:
            while rear:
                front = front.push(rear.peek())
                rear = rear.pop()
        return Queue(front, rear)
