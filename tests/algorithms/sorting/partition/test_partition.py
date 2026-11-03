from algorithms.sorting import partition
from tests.support import Ordered


def test_partition_is_confined_to_range_and_preserves_payloads() -> None:
    values = [Ordered(value, str(i)) for i, value in enumerate([99, 4, 1, 3, 3, 2, -99])]
    original = values.copy()
    equal_left, equal_right = partition.partition(values, 1, 6, 3)
    assert values[0] is original[0] and values[-1] is original[-1]
    assert all(value.value < 3 for value in values[1:equal_left])
    assert [value.value for value in values[equal_left:equal_right]] == [3, 3]
    assert all(3 < value.value for value in values[equal_right:6])
    assert {id(value) for value in values} == {id(value) for value in original}
