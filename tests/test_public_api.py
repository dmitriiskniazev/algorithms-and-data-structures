import importlib
import inspect

import pytest


@pytest.mark.parametrize(
    ("name", "package", "operations"),
    [
        ("algorithms.dynamic_programming.fibonacci", True, ("recursive", "memoized", "tabulated", "constant_space")),
        ("algorithms.sorting.quick_sort", True, ("recursive", "iterative")),
        ("algorithms.selection.order_statistic", True, ("recursive", "iterative", "by_sorting")),
        ("algorithms.searching.binary_search", True, ("equal_range", "search")),
        ("algorithms.searching.binary_search.lower_bound", True, ("iterative", "recursive")),
        ("algorithms.searching.binary_search.upper_bound", True, ("iterative", "recursive")),
        ("algorithms.sorting.bubble_sort", False, ("sort",)),
        ("algorithms.strings.suffix_array", False, ("build",)),
        ("algorithms.graphs.dijkstra", False, ("shortest_paths",)),
    ],
)
def test_algorithm_namespace(name: str, package: bool, operations: tuple[str, ...]) -> None:
    module = importlib.import_module(name)
    assert inspect.ismodule(module)
    assert hasattr(module, "__path__") is package
    for name in operations:
        operation = getattr(module, name)
        assert inspect.isfunction(operation)
        assert operation.__name__ == name


@pytest.mark.parametrize(
    ("name", "class_name"),
    [
        ("data_structures.stack.dynamic_array", "Stack"),
        ("data_structures.stack.fixed_array", "Stack"),
        ("data_structures.stack.linked_list", "Stack"),
        ("data_structures.stack.two_queues", "Stack"),
        ("data_structures.stack.persistent", "Stack"),
        ("data_structures.queue.two_stacks", "Queue"),
        ("data_structures.queue.persistent", "Queue"),
        ("data_structures.deque", "Deque"),
        ("data_structures.priority_queue.minimum", "PriorityQueue"),
        ("data_structures.priority_queue.maximum", "PriorityQueue"),
        ("data_structures.queue.extrema.minimum", "Queue"),
        ("data_structures.stack.extrema.minimum", "Stack"),
        ("data_structures.stack.extrema.maximum", "Stack"),
        ("data_structures.queue.extrema.maximum", "Queue"),
    ],
)
def test_structure_namespace(name: str, class_name: str) -> None:
    module = importlib.import_module(name)
    assert not hasattr(module, "__path__")
    structure = getattr(module, class_name)
    assert inspect.isclass(structure)
    assert structure.__module__ == name
    assert structure.__name__ == class_name


def test_old_facade_aliases_are_removed() -> None:
    import algorithms.dynamic_programming as dynamic_programming
    import algorithms.sorting as sorting
    import data_structures
    from algorithms.dynamic_programming import fibonacci
    from algorithms.sorting import quick_sort
    from data_structures import stack as stacks

    for namespace, names in [
        (fibonacci, ("fibonacci", "fibonacci_recursive", "fibonacci_memoized", "fibonacci_tabulated")),
        (quick_sort, ("quick_sort", "quick_sort_recursive")),
        (dynamic_programming, ("lcs", "edit_alignment")),
        (sorting, ("quick_sort_recursive",)),
        (stacks, ("min_max",)),
        (data_structures, ("ArrayStack", "FixedArrayStack", "PersistentStack", "PersistentQueue", "ChainedHashMap")),
    ]:
        assert all(not hasattr(namespace, name) for name in names)
