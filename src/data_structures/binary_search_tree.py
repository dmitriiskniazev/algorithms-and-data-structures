from collections.abc import Iterator
from typing import Literal

from algorithms.comparable import Comparable


class _Node[T]:
    __slots__ = ("key", "left", "right")

    def __init__(self, key: T) -> None:
        self.key = key
        self.left: _Node[T] | None = None
        self.right: _Node[T] | None = None


class BinarySearchTree[T: Comparable]:
    def __init__(self) -> None:
        self.root: _Node[T] | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _find_node(self, key: T) -> tuple[_Node[T] | None, _Node[T] | None]:
        parent: _Node[T] | None = None
        node = self.root
        while node is not None:
            if key < node.key:
                parent, node = node, node.left
            elif node.key < key:
                parent, node = node, node.right
            else:
                break
        return parent, node

    def search(self, key: T) -> bool:
        _, node = self._find_node(key)
        return node is not None

    def insert(self, key: T) -> bool:
        parent, node = self._find_node(key)
        if node is not None:
            return False
        node = _Node(key)
        if parent is None:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self._size += 1
        return True

    def delete(self, key: T) -> bool:
        parent, node = self._find_node(key)
        if node is None:
            return False
        if node.left is not None and node.right is not None:
            successor_parent, successor = node, node.right
            while successor.left is not None:
                successor_parent, successor = successor, successor.left
            node.key = successor.key
            parent, node = successor_parent, successor
        child = node.left if node.left is not None else node.right
        self._replace_child(parent, node, child)
        self._size -= 1
        return True

    def _replace_child(self, parent: _Node[T] | None, node: _Node[T], child: _Node[T] | None) -> None:
        if parent is None:
            self.root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child

    def _traverse(self, order: Literal["preorder", "inorder", "postorder"]) -> Iterator[T]:
        stack: list[tuple[_Node[T], bool]] = []
        if self.root is not None:
            stack.append((self.root, False))
        while stack:
            node, visit = stack.pop()
            if visit:
                yield node.key
            elif order == "preorder":
                yield node.key
                if node.right is not None:
                    stack.append((node.right, False))
                if node.left is not None:
                    stack.append((node.left, False))
            elif order == "inorder":
                if node.right is not None:
                    stack.append((node.right, False))
                stack.append((node, True))
                if node.left is not None:
                    stack.append((node.left, False))
            else:
                stack.append((node, True))
                if node.right is not None:
                    stack.append((node.right, False))
                if node.left is not None:
                    stack.append((node.left, False))

    def inorder(self) -> tuple[T, ...]:
        return tuple(self._traverse("inorder"))

    def preorder(self) -> tuple[T, ...]:
        return tuple(self._traverse("preorder"))

    def postorder(self) -> tuple[T, ...]:
        return tuple(self._traverse("postorder"))
