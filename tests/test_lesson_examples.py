import re
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parents[1] / "docs"
LESSONS = sorted([*(DOCS / "algorithms").glob("*.md"), *(DOCS / "data-structures").glob("*.md")])


@pytest.mark.parametrize("path", LESSONS, ids=lambda path: path.stem)
def test_lesson_starts_with_an_executable_contract(path: Path) -> None:
    text = path.read_text()
    first_source = text.find("{literalinclude}")
    brief = text[:first_source] if first_source != -1 else text
    assert "**Вход.**" in brief and "**Результат.**" in brief
    assert "**Предусловия.**" in brief
    check = re.search(r"### Проверка.*?```python\n(.*?)```", brief, re.S)
    assert check is not None, path
    exec(compile(check.group(1), str(path), "exec"), {})
