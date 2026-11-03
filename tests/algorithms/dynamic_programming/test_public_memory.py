import tracemalloc
from collections.abc import Callable
from importlib import import_module

import pytest


def peak_bytes(compute: Callable[[], object]) -> int:
    tracemalloc.start()
    try:
        result = compute()
        assert result is not None
        return tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()


@pytest.mark.parametrize("kind", ("knapsack_01", "longest_common_subsequence", "edit_distance"))
def test_public_reconstruction_uses_less_memory_than_numeric_table(kind: str) -> None:
    module = import_module(f"algorithms.dynamic_programming.{kind}")
    if kind == "knapsack_01":
        args = ([1] * 160, list(range(160)), 160)
        public = module.solve
        table = module.build_table
    else:
        args = ("ab" * 80, "ba" * 80)
        public = module.solve if kind == "longest_common_subsequence" else module.align
        table = module.build_table
    # Compare complete public reconstruction with even just the old numeric table.
    # A broad relative bound avoids depending on exact allocator/object sizes.
    # Exclude one-time lazy imports from the algorithm's allocation measurement.
    public(*args)
    assert peak_bytes(lambda: public(*args)) < 0.6 * peak_bytes(lambda: table(*args))
