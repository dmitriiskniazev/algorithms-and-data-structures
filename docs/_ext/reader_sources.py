"""Collect actual lesson source files and their local dependencies for the reader."""

import ast
import json
from collections import deque
from html import escape
from pathlib import Path
from typing import TypedDict

from docutils import nodes
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import STANDARD_TYPES


class Source(TypedDict):
    path: str
    name: str
    group: str
    code: str
    lines: list[str]
    common: bool


def highlighted_lines(code: str) -> list[str]:
    lines = [""]
    for kind, value in lex(code, PythonLexer(ensurenl=False, stripnl=False)):
        while kind not in STANDARD_TYPES:
            kind = kind.parent
        css = STANDARD_TYPES[kind]
        for i, part in enumerate(value.split("\n")):
            if i:
                lines.append("")
            if part:
                text = escape(part)
                lines[-1] += f'<span class="{css}">{text}</span>' if css else text
    if code.endswith("\n"):
        lines.pop()
    return lines


def resolve_module(src: Path, name: str) -> Path | None:
    if not name.startswith(("algorithms", "data_structures")):
        return None
    path = src.joinpath(*name.split("."))
    for candidate in [path.with_suffix(".py"), path / "__init__.py"]:
        if candidate.is_file():
            return candidate
    return None


def dependencies(src: Path, path: Path) -> list[Path]:
    parts = list(path.relative_to(src).with_suffix("").parts)
    package = parts[:-1]
    result: list[Path] = []
    for node in ast.walk(ast.parse(path.read_text())):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = package[: len(package) - node.level + 1] if node.level else []
            module = ".".join([*base, *([node.module] if node.module else [])])
            names = [module, *(f"{module}.{alias.name}" for alias in node.names)]
        for name in names:
            target = resolve_module(src, name)
            if target is not None and target not in result:
                result.append(target)
    return result


def collect_sources(root: Path, doctree: nodes.document | None) -> list[Source]:
    if doctree is None:
        return []
    src = root / "src"
    initial = []
    for block in doctree.findall(nodes.literal_block):
        title = block.get("course_path", "")
        if title.startswith("src/"):
            path = root / title
            if path.is_file() and path not in initial:
                initial.append(path)
    queue = deque(initial)
    seen: set[Path] = set()
    result: list[Source] = []
    while queue:
        path = queue.popleft()
        if path in seen:
            continue
        seen.add(path)
        code = path.read_text()
        common = path not in initial or path.stem in {"__init__", "_types", "_common", "directions"}
        result.append(
            {
                "path": path.relative_to(root).as_posix(),
                "name": path.stem if path.stem == "__init__" else path.stem.removeprefix("_"),
                "group": ".".join(path.parent.relative_to(src).parts),
                "code": code,
                "lines": highlighted_lines(code),
                "common": common,
            }
        )
        queue.extend(dependencies(src, path))
    return result


def sources_json(root: Path, doctree: nodes.document | None) -> str:
    return (
        json.dumps(collect_sources(root, doctree), ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )
