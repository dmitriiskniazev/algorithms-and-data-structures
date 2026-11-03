from data_structures import heap
from tests.support import Ordered


def assert_heap(values) -> None:
    assert all(not values[(i - 1) // 2] < values[i] for i in range(1, len(values)))


def test_build_and_restore_max_heap() -> None:
    values = [Ordered(i) for i in [3, 1, 8, 2, 5]]
    identities = {id(value) for value in values}
    heap.build(values)
    assert_heap(values)
    assert {id(value) for value in values} == identities
    values.append(Ordered(9))
    heap.sift_up(values, len(values) - 1)
    assert_heap(values)
    values[0] = Ordered(0)
    heap.sift_down(values, 0, len(values))
    assert_heap(values)
    heap.build([])
    heap.sift_down([], 0, 0)
