import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("name", ["accepted", "rejected"])
def test_type_contracts(name: str) -> None:
    fixture = Path(__file__).with_name(f"{name}.py")
    result = subprocess.run(
        [sys.executable, "-m", "pyright", "--outputjson", str(fixture)], cwd=ROOT, capture_output=True, text=True
    )
    report = json.loads(result.stdout)
    errors = [item for item in report["generalDiagnostics"] if item["severity"] == "error"]
    if name == "accepted":
        assert result.returncode == 0, result.stdout + result.stderr
        assert not errors
        return
    expected = {i for i, line in enumerate(fixture.read_text().splitlines()) if "# error" in line}
    actual = {item["range"]["start"]["line"] for item in errors if Path(item["file"]) == fixture}
    assert result.returncode == 1, result.stdout + result.stderr
    assert actual == expected, result.stdout
    assert all(Path(item["file"]) == fixture for item in errors), result.stdout
