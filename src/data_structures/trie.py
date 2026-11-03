class _Node:
    __slots__ = ("children", "terminal")

    def __init__(self) -> None:
        self.children: dict[str, _Node] = {}
        self.terminal = False


class Trie:
    def __init__(self) -> None:
        self._root = _Node()

    def insert(self, word: str) -> None:
        node = self._root
        for symbol in word:
            child = node.children.get(symbol)
            if child is None:
                child = _Node()
                node.children[symbol] = child
            node = child
        node.terminal = True

    def _walk(self, text: str) -> _Node | None:
        node = self._root
        for symbol in text:
            node = node.children.get(symbol)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.terminal

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
