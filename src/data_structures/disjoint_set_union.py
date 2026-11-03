class DisjointSetUnion:
    def __init__(self, size: int) -> None:
        if size < 0:
            raise ValueError("size must be nonnegative")
        self._parent = list(range(size))
        self._size = [1] * size
        self._components = size

    def __len__(self) -> int:
        return len(self._parent)

    @property
    def components(self) -> int:
        return self._components

    def find(self, item: int) -> int:
        if not 0 <= item < len(self):
            raise IndexError("item outside the universe")
        root = item
        while self._parent[root] != root:
            root = self._parent[root]
        while item != root:
            parent = self._parent[item]
            self._parent[item] = root
            item = parent
        return root

    def union(self, first: int, second: int) -> bool:
        left, right = self.find(first), self.find(second)
        if left == right:
            return False
        if self._size[left] < self._size[right]:
            left, right = right, left
        self._parent[right] = left
        self._size[left] += self._size[right]
        self._components -= 1
        return True

    def connected(self, first: int, second: int) -> bool:
        return self.find(first) == self.find(second)
