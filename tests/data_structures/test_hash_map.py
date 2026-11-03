from data_structures import hash_map


class CollisionKey:
    def __init__(self, value: int) -> None:
        self.value = value

    def __hash__(self) -> int:
        return 1

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CollisionKey) and self.value == other.value


def test_collisions_updates_deletion_and_resize() -> None:
    table: hash_map.HashMap[CollisionKey, int] = hash_map.HashMap()
    first, second = CollisionKey(1), CollisionKey(2)
    assert table.set(first, 10)
    assert table.set(second, 20)
    assert not table.set(CollisionKey(1), 11)
    assert table.get(first) == 11 and table.get(second) == 20
    for key in range(100):
        table.set(key, key * 2)
    assert len(table) == 102
    assert table.get(second) == 20
    assert table.delete(first) and not table.delete(first)
    assert table.get(second) == 20
    assert len(list(table.items())) == len(table)
