import ast
import importlib
import inspect
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
SHARED: set[str] = set()


def test_initializers_only_assemble_public_imports() -> None:
    for path in SRC.rglob("__init__.py"):
        for node in ast.parse(path.read_text()).body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            if (
                isinstance(node, ast.Expr)
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)
            ):
                continue
            assert isinstance(node, ast.Assign), (path, ast.dump(node))
            assert all(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets), path
            assert isinstance(ast.literal_eval(node.value), list), path


def test_each_teaching_operation_has_its_own_source_file() -> None:
    for path in SRC.rglob("*.py"):
        if path.name in {"__init__.py", "_types.py", "_common.py"} or str(path.relative_to(SRC)) in SHARED:
            continue
        tree = ast.parse(path.read_text())
        operations = {
            node.name for node in tree.body if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
        }
        assert len(operations) <= 1, (path, operations)
        structures = {
            node.name for node in tree.body if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
        }
        assert len(structures) <= 1, (path, structures)


def test_all_facade_exports_exist_and_operations_use_distinct_files() -> None:
    implementations: dict[str, str] = {}
    for path in SRC.rglob("__init__.py"):
        name = ".".join(path.parent.relative_to(SRC).parts)
        module = importlib.import_module(name)
        for public_name in module.__all__:
            operation = getattr(module, public_name)
            if inspect.isfunction(operation):
                assert operation.__name__ == public_name
                filename = inspect.getfile(operation)
                assert Path(filename).is_relative_to(SRC)
                previous = implementations.setdefault(filename, operation.__name__)
                assert previous == operation.__name__, (filename, previous, operation.__name__)


def test_algorithms_and_structures_use_their_categories() -> None:
    from algorithms import divide_and_conquer, sorting, strings
    from data_structures import trie

    assert not hasattr(divide_and_conquer, "merge_sort")
    assert sorting.merge_sort.sort.__module__ == "algorithms.sorting.merge_sort"

    assert not hasattr(strings, "trie")
    assert trie.Trie.__module__ == "data_structures.trie"
