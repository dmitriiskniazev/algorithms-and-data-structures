class IndexedHeap:
    def __init__(self, n: int) -> None:
        self.values: list[tuple[int, int]] = []
        self.pos = [-1] * n

    def __len__(self) -> int:
        return len(self.values)

    def push_or_decrease(self, vertex: int, weight: int) -> None:
        i = self.pos[vertex]
        if i == -1:
            i = len(self.values)
            self.pos[vertex] = i
            self.values.append((weight, vertex))
        else:
            self.values[i] = (weight, vertex)
        self._sift_up(i)

    def pop(self) -> tuple[int, int]:
        value = self.values[0]
        last = self.values.pop()
        self.pos[value[1]] = -1
        if self.values:
            self.values[0] = last
            self.pos[last[1]] = 0
            self._sift_down(0)
        return value

    def _swap(self, first: int, second: int) -> None:
        self.values[first], self.values[second] = self.values[second], self.values[first]
        self.pos[self.values[first][1]] = first
        self.pos[self.values[second][1]] = second

    def _sift_up(self, child: int) -> None:
        while child:
            parent = (child - 1) // 2
            if not self.values[child] < self.values[parent]:
                break
            self._swap(parent, child)
            child = parent

    def _sift_down(self, root: int) -> None:
        while True:
            left = 2 * root + 1
            right = left + 1
            smallest = root
            if left < len(self.values) and self.values[left] < self.values[smallest]:
                smallest = left
            if right < len(self.values) and self.values[right] < self.values[smallest]:
                smallest = right
            if smallest == root:
                return
            self._swap(root, smallest)
            root = smallest
