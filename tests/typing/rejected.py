from dataclasses import dataclass

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
from data_structures import binary_search_tree, hash_map, interfaces, priority_queue
from data_structures import queue as queues
from data_structures import stack as stacks


@dataclass
class Record:
    name: str
    priority: int


records = [Record("a", 1)]
bubble_sort.sort(records)  # error
insertion_sort.sort(records)  # error
selection_sort.sort(records)  # error
merge_sort.sort(records)  # error
heap_sort.sort(records)  # error
quick_sort.iterative(records)  # error
quick_sort.recursive(records)  # error
order_statistic.iterative(records, 0)  # error
order_statistic.recursive(records, 0)  # error
order_statistic.by_sorting(records, 0)  # error
median.find(records)  # error
inversions.count(records)  # error
binary_search.search(records, Record("a", 1))  # error
binary_search.lower_bound.iterative(records, Record("a", 1))  # error
binary_search.lower_bound.recursive(records, Record("a", 1))  # error
binary_search.upper_bound.iterative(records, Record("a", 1))  # error
binary_search.upper_bound.recursive(records, Record("a", 1))  # error
binary_search.equal_range(records, Record("a", 1))  # error
binary_search.lower_bound.iterative(records, 1, key=lambda record: record)  # error
binary_search.lower_bound.recursive(records, 1, key=lambda record: record)  # error
binary_search.upper_bound.iterative(records, 1, key=lambda record: record)  # error
binary_search.upper_bound.recursive(records, 1, key=lambda record: record)  # error
binary_search.equal_range(records, 1, key=lambda record: record)  # error
bubble_sort.sort(records, key=lambda record: record)  # error
counting_sort.sort(records)  # error
radix_sort.sort(records)  # error
counting_sort.sort(records, key=lambda record: record.name)  # error
radix_sort.sort(records, key=lambda record: record.name)  # error
stacks.extrema.minimum.Stack[Record]()  # error
queues.extrema.minimum.Queue[Record]()  # error
priority_queue.minimum.PriorityQueue[Record]()  # error
binary_search_tree.BinarySearchTree[Record]()  # error
hash_map.HashMap[list[int], str]()  # error
stacks.persistent.Stack[int]().push("wrong value")  # error


mutable_stack: interfaces.Stack[int] = stacks.persistent.Stack[int]()  # error
persistent_stack: interfaces.PersistentStack[int] = stacks.dynamic_array.Stack[int]()  # error
mutable_queue: interfaces.Queue[int] = queues.persistent.Queue[int]()  # error
persistent_queue: interfaces.PersistentQueue[int] = queues.ring.Queue[int]()  # error
wrong_value: interfaces.Stack[str] = stacks.dynamic_array.Stack[int]()  # error


class WrongPop:
    def __len__(self) -> int:
        return 0

    def push(self, value: int) -> None:
        pass

    def peek(self) -> int:
        return 0

    def pop(self) -> str:
        return "wrong"


wrong_result: interfaces.Stack[int] = WrongPop()  # error
