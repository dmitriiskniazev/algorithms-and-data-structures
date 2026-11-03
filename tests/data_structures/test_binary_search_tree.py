from data_structures import binary_search_tree


def test_traversals_search_insert_and_all_delete_shapes() -> None:
    tree = binary_search_tree.BinarySearchTree[int]()
    for key in (8, 3, 10, 1, 6, 14, 4, 7, 13):
        assert tree.insert(key)
    assert not tree.insert(6)
    assert tree.inorder() == (1, 3, 4, 6, 7, 8, 10, 13, 14)
    assert tree.preorder() == (8, 3, 1, 6, 4, 7, 10, 14, 13)
    assert tree.postorder() == (1, 4, 7, 6, 3, 13, 14, 10, 8)
    assert tree.search(13) and not tree.search(5)
    assert tree.delete(3)  # two children: successor 4
    assert tree.delete(14)  # one child
    assert tree.delete(1)  # leaf
    assert not tree.delete(99)
    assert tree.inorder() == (4, 6, 7, 8, 10, 13)
    assert len(tree) == 6


def test_empty_and_degenerate_tree() -> None:
    tree = binary_search_tree.BinarySearchTree[int]()
    assert tree.inorder() == tree.preorder() == tree.postorder() == ()
    for key in range(20):
        assert tree.insert(key)
    assert tree.inorder() == tuple(range(20))
    for key in range(20):
        assert tree.delete(key)
    assert len(tree) == 0


def test_order_equivalence_without_equality() -> None:
    from tests.support import Ordered

    tree = binary_search_tree.BinarySearchTree[Ordered]()
    for value in [8, 3, 10, 1, 6, 4, 7]:
        assert tree.insert(Ordered(value))
    assert not tree.insert(Ordered(6, "duplicate"))
    assert tree.search(Ordered(6, "different object"))
    assert tree.delete(Ordered(3))
    assert not tree.search(Ordered(3))
    assert [value.value for value in tree.inorder()] == [1, 4, 6, 7, 8, 10]
