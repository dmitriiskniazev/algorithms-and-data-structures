import hashlib
import importlib.util
import json
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path

import pytest
from docutils import nodes
from docutils.utils import new_document

ROOT = Path(__file__).resolve().parents[2]


def source_module():
    path = ROOT / "docs/_ext/reader_sources.py"
    spec = importlib.util.spec_from_file_location("reader_sources_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_complete_sources_include_local_dependencies_and_preserve_text() -> None:
    module = source_module()
    doc = new_document("lesson")
    for path in [
        "src/algorithms/searching/binary_search/lower_bound/_recursive.py",
        "src/data_structures/queue/extrema/minimum.py",
    ]:
        block = nodes.literal_block()
        block["course_path"] = path
        doc += block
    sources = module.collect_sources(ROOT, doc)
    paths = {source["path"] for source in sources}
    assert "src/algorithms/comparable.py" in paths
    assert "src/data_structures/stack/extrema/minimum.py" in paths
    assert "src/data_structures/stack/extrema/_types.py" in paths
    for source in sources:
        assert source["code"] == (ROOT / source["path"]).read_text()


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.text = ""

    def handle_data(self, data: str) -> None:
        self.text += data


def test_highlighted_lines_preserve_every_python_source() -> None:
    module = source_module()
    for path in (ROOT / "src").rglob("*.py"):
        code = path.read_text()
        parser = Text()
        lines = module.highlighted_lines(code)
        parser.feed("\n".join(lines) + ("\n" if code.endswith("\n") else ""))
        assert parser.text == code, path


def test_all_shipped_font_faces_match_the_catalog() -> None:
    root = ROOT / "docs/_static/fonts"
    fonts = json.loads((root / "catalog.json").read_text())
    assert len(fonts) == 9
    for font in fonts:
        for face in font["faces"]:
            data = (root / face["file"]).read_bytes()
            assert hashlib.sha256(data).hexdigest() == face["sha256"]
            assert len(data) == face["bytes"] and face["russian"]


@pytest.mark.skipif(shutil.which("node") is None, reason="Node is needed for JavaScript model checks")
def test_reader_selection_and_settings_models() -> None:
    result = subprocess.run(
        ["node", str(Path(__file__).with_name("reader_models.mjs"))], cwd=ROOT, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(shutil.which("node") is None, reason="Node is needed for JavaScript syntax checks")
def test_all_reader_modules_parse() -> None:
    for path in [*(ROOT / "docs/_static/reader").rglob("*.js"), ROOT / "docs/_static/course-code.mjs"]:
        result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
