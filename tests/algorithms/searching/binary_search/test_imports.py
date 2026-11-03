import subprocess
import sys

import pytest


@pytest.mark.parametrize("operation", ["lower_bound", "upper_bound"])
@pytest.mark.parametrize("variant", ["iterative", "recursive"])
@pytest.mark.parametrize("direct_first", [False, True])
def test_public_variant_survives_direct_implementation_import(operation: str, variant: str, direct_first: bool) -> None:
    direct = f"from algorithms.searching.binary_search.{operation}._{variant} import {variant}\n"
    public = "from algorithms.searching import binary_search\n"
    code = (
        (direct + public if direct_first else public + direct)
        + f"""
import inspect
from pathlib import Path
namespace = binary_search.{operation}
assert namespace.{variant} is {variant}
assert inspect.isfunction(namespace.{variant})
assert Path(inspect.getfile(namespace.{variant})).name == "_{variant}.py"
assert namespace.{variant}([1, 2, 2, 5], 2) == {1 if operation == "lower_bound" else 3}
assert binary_search.equal_range([1, 2, 2, 5], 2) == (1, 3)
assert binary_search.search([1, 2, 2, 5], 2) == 1
"""
    )
    result = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_old_category_does_not_export_binary_search() -> None:
    import algorithms.divide_and_conquer as divide_and_conquer

    assert not hasattr(divide_and_conquer, "binary_search")
