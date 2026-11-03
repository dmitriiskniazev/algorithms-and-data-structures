import pytest

from data_structures import disjoint_set_union


def test_union_connectivity_and_component_count() -> None:
    sets = disjoint_set_union.DisjointSetUnion(6)
    assert sets.components == 6
    assert sets.union(0, 1)
    assert sets.union(1, 2)
    assert not sets.union(0, 2)
    assert sets.connected(0, 2)
    assert not sets.connected(0, 3)
    assert sets.components == 4


def test_invalid_size_and_elements() -> None:
    with pytest.raises(ValueError):
        disjoint_set_union.DisjointSetUnion(-1)
    with pytest.raises(IndexError):
        disjoint_set_union.DisjointSetUnion(2).find(2)
