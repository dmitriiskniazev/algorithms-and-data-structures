from algorithms.comparable import Comparable


class PriorityQueue[T: Comparable]:
    def __init__(self) -> None:
        self.values: list[T] = []

    def __len__(self) -> int:
        return len(self.values)

    def push(self, value: T) -> None:
        self.values.append(value)
        self._sift_up(len(self.values) - 1)

    def peek(self) -> T:
        if not self.values:
            raise IndexError("empty priority queue")
        return self.values[0]

    def pop(self) -> T:
        value = self.peek()
        last = self.values.pop()
        if self.values:
            self.values[0] = last
            self._sift_down(0)
        return value

    def _sift_up(self, child: int) -> None:
        while child:
            parent = (child - 1) // 2
            if not self.values[child] < self.values[parent]:
                break
            self.values[parent], self.values[child] = self.values[child], self.values[parent]
            child = parent

    def _sift_down(self, root: int) -> None:
        right = len(self.values)
        while 2 * root + 1 < right:
            child = 2 * root + 1
            if child + 1 < right and self.values[child + 1] < self.values[child]:
                child += 1
            if not self.values[child] < self.values[root]:
                break
            self.values[root], self.values[child] = self.values[child], self.values[root]
            root = child
