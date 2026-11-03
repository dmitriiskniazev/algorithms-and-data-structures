from algorithms.comparable import Comparable
from data_structures.heap import sift_down, sift_up


class PriorityQueue[T: Comparable]:
    def __init__(self) -> None:
        self.values: list[T] = []

    def __len__(self) -> int:
        return len(self.values)

    def push(self, value: T) -> None:
        self.values.append(value)
        sift_up(self.values, len(self.values) - 1)

    def peek(self) -> T:
        if not self.values:
            raise IndexError("empty priority queue")
        return self.values[0]

    def pop(self) -> T:
        value = self.peek()
        last = self.values.pop()
        if self.values:
            self.values[0] = last
            sift_down(self.values, 0, len(self.values))
        return value
