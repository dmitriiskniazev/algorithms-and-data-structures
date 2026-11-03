from dataclasses import dataclass
from typing import Self, assert_type

from algorithms.divide_and_conquer import inversions
from algorithms.searching import binary_search
from algorithms.selection import median, order_statistic
from algorithms.sorting import (
    bubble_sort,
    counting_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    radix_sort,
    selection_sort,
)
from data_structures import binary_search_tree, deque, disjoint_set_union, hash_map, interfaces, priority_queue, trie
from data_structures import queue as queues
from data_structures import stack as stacks


@dataclass
class Record:
    name: str
    priority: int

    def __lt__(self, other: Self, /) -> bool:
        return self.priority < other.priority


class Ranked:
    def __init__(self, value: int) -> None:
        self.value = value

    def __lt__(self, other: Self, /) -> bool:
        return self.value < other.value


def accepts_ordered_values() -> None:
    values = [3, 1, 2]
    assert_type(bubble_sort.sort(values), None)
    assert_type(insertion_sort.sort(values), None)
    assert_type(selection_sort.sort(values), None)
    assert_type(merge_sort.sort(values), None)
    assert_type(heap_sort.sort(values), None)
    assert_type(quick_sort.iterative(values), None)
    assert_type(quick_sort.recursive(values), None)
    assert_type(counting_sort.sort(values), None)
    assert_type(radix_sort.sort(values), None)
    assert_type(order_statistic.iterative(values, 0), int)
    assert_type(order_statistic.recursive(values, 0), int)
    assert_type(order_statistic.by_sorting(values, 0), int)
    assert_type(median.find(values), tuple[int, int])
    assert_type(inversions.count(values), int)
    assert_type(binary_search.search(values, 2), int | None)
    assert_type(binary_search.lower_bound.iterative(values, 2), int)
    assert_type(binary_search.lower_bound.recursive(values, 2), int)
    assert_type(binary_search.upper_bound.iterative(values, 2), int)
    assert_type(binary_search.upper_bound.recursive(values, 2), int)
    assert_type(binary_search.equal_range(values, 2), tuple[int, int])
    assert_type(order_statistic.iterative([Ranked(1)], 0), Ranked)
    bubble_sort.sort([Ranked(1)])
    stack = stacks.extrema.minimum.Stack[int]()
    stack.push(3)
    assert_type(stack.extreme(), int)
    assert_type(priority_queue.minimum.PriorityQueue[int]().pop(), int)
    assert_type(queues.extrema.minimum.Queue[int]().extreme(), int)


def accepts_ordered_records() -> None:
    records = [Record("b", 2), Record("a", 1)]
    assert_type(bubble_sort.sort(records), None)
    assert_type(insertion_sort.sort(records), None)
    assert_type(selection_sort.sort(records), None)
    assert_type(merge_sort.sort(records), None)
    assert_type(heap_sort.sort(records), None)
    assert_type(quick_sort.iterative(records), None)
    assert_type(quick_sort.recursive(records), None)
    assert_type(order_statistic.iterative(records, 0), Record)
    assert_type(order_statistic.recursive(records, 0), Record)
    assert_type(order_statistic.by_sorting(records, 0), Record)
    assert_type(median.find(records), tuple[Record, Record])
    assert_type(inversions.count(records), int)
    assert_type(binary_search.search(records, Record("target", 1)), int | None)
    assert_type(binary_search.lower_bound.iterative(records, Record("target", 1)), int)
    assert_type(binary_search.lower_bound.recursive(records, Record("target", 1)), int)
    assert_type(binary_search.upper_bound.iterative(records, Record("target", 1)), int)
    assert_type(binary_search.upper_bound.recursive(records, Record("target", 1)), int)
    assert_type(binary_search.equal_range(records, Record("target", 1)), tuple[int, int])
    assert_type(stacks.extrema.minimum.Stack[Record]().extreme(), Record)
    assert_type(queues.extrema.minimum.Queue[Record]().extreme(), Record)
    assert_type(priority_queue.minimum.PriorityQueue[Record]().pop(), Record)


def preserves_container_values() -> None:
    assert_type(stacks.persistent.Stack[Record]().push(Record("a", 1)).peek(), Record)
    assert_type(queues.persistent.Queue[Record]().push(Record("a", 1)).peek(), Record)
    assert_type(binary_search_tree.BinarySearchTree[Ranked]().inorder(), tuple[Ranked, ...])
    assert_type(hash_map.HashMap[str, Record]().get("a"), Record)


# Structural assignments check every implementation; inheritance is not required.
def accepts_structure_interfaces() -> None:
    stack_values: list[interfaces.Stack[int]] = [
        stacks.dynamic_array.Stack[int](),
        stacks.fixed_array.Stack[int](capacity=10),
        stacks.linked_list.Stack[int](),
        stacks.one_queue.Stack[int](),
        stacks.two_queues.Stack[int](),
        stacks.extrema.minimum.Stack[int](),
        stacks.extrema.maximum.Stack[int](),
    ]
    queue_values: list[interfaces.Queue[int]] = [
        queues.linked_list.Queue[int](),
        queues.ring.Queue[int](),
        queues.two_stacks.Queue[int](),
        queues.extrema.minimum.Queue[int](),
        queues.extrema.maximum.Queue[int](),
    ]
    for stack in stack_values:
        stack.push(1)
        assert_type(stack.peek(), int)
        assert_type(stack.pop(), int)
    for queue in queue_values:
        queue.push(1)
        assert_type(queue.peek(), int)
        assert_type(queue.pop(), int)
    priorities: list[interfaces.PriorityQueue[Record]] = [
        priority_queue.minimum.PriorityQueue[Record](),
        priority_queue.maximum.PriorityQueue[Record](),
    ]
    for priority in priorities:
        priority.push(Record("a", 1))
        assert_type(priority.pop(), Record)
    extrema: list[interfaces.ExtremaQueue[Record]] = [
        queues.extrema.minimum.Queue[Record](),
        queues.extrema.maximum.Queue[Record](),
    ]
    for queue in extrema:
        assert_type(queue.extreme(), Record)
    minimum: interfaces.ExtremaStack[Record] = stacks.extrema.minimum.Stack[Record]()
    assert_type(minimum.extreme(), Record)
    maximum: interfaces.ExtremaStack[Record] = stacks.extrema.maximum.Stack[Record]()
    assert_type(maximum.extreme(), Record)
    double: interfaces.Deque[Record] = deque.Deque[Record]()
    double.push_front(Record("a", 1))
    assert_type(double.pop_back(), Record)
    tree: interfaces.BinarySearchTree[Record] = binary_search_tree.BinarySearchTree[Record]()
    assert_type(tree.inorder(), tuple[Record, ...])
    mapping: interfaces.HashMap[str, Record] = hash_map.HashMap[str, Record]()
    assert_type(mapping.get("a"), Record)
    sets: interfaces.DisjointSetUnion = disjoint_set_union.DisjointSetUnion(10)
    assert_type(sets.components, int)
    words: interfaces.Trie = trie.Trie()
    assert_type(words.search("word"), bool)


def preserves_persistent_interfaces() -> None:
    stack: interfaces.PersistentStack[Record] = stacks.persistent.Stack[Record]()
    queue: interfaces.PersistentQueue[Record] = queues.persistent.Queue[Record]()
    assert_type(stack.push(Record("a", 1)).pop().peek(), Record)
    assert_type(queue.push(Record("a", 1)).pop().peek(), Record)
    # Self also preserves the concrete implementation at the call site.
    assert_type(stacks.persistent.Stack[int]().push(1).pop(), stacks.persistent.Stack[int])
    assert_type(queues.persistent.Queue[int]().push(1).pop(), queues.persistent.Queue[int])
