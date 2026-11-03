from algorithms.dynamic_programming.edit_distance._build_parents import build_parents
from algorithms.dynamic_programming.edit_distance._restore_from_parents import restore_from_parents
from algorithms.dynamic_programming.edit_distance._types import Edit


def align(source: str, target: str) -> tuple[int, list[Edit]]:

    val, parent = build_parents(source, target)
    return val, restore_from_parents(source, target, parent)
