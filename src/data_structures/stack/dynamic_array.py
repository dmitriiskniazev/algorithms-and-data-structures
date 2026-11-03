class Stack[T]:
    def __init__(self) -> None:
        self.values: list[T] = []

    def __len__(self) -> int:
        return len(self.values)

    def push(self, value: T) -> None:
        self.values.append(value)

    def peek(self) -> T:
        if not self.values:
            raise IndexError("empty stack")
        return self.values[-1]

    def pop(self) -> T:
        self.peek()
        return self.values.pop()
