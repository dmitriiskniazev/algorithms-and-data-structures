import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    "imports",
    [
        "import algorithms.sorting.heap_sort; import data_structures",
        "import data_structures; import algorithms.sorting.heap_sort",
    ],
)
def test_heap_sort_facade_is_independent_of_import_order(imports: str) -> None:
    code = (
        imports
        + """
from algorithms.sorting import heap_sort
values = [3, 1, 2]
heap_sort.sort(values)
assert values == [1, 2, 3]
"""
    )
    result = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
