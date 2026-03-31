from __future__ import annotations

import runpy
import sys
from pathlib import Path
from uuid import uuid4

import pytest


def test_script_viz_loads_staging_path_and_calls_norm_runner(monkeypatch) -> None:
    root_dir = Path(__file__).resolve().parents[1]
    staging_path = root_dir / ".local_tmp" / "tests" / "viz" / uuid4().hex
    staging_path.mkdir(parents=True, exist_ok=True)
    report_path = staging_path / "norm_report.txt"
    report_path.write_text("", encoding="utf-8")

    calls: list[Path] = []

    monkeypatch.setattr(sys, "argv", ["viz.py", "-norm", str(staging_path)])
    monkeypatch.syspath_prepend(str(root_dir / "src"))
    import data_preprocessor.visualize as visualize

    monkeypatch.setattr(visualize, "norms", lambda path: calls.append(Path(path)))

    with pytest.raises(SystemExit) as excinfo:
        runpy.run_path(str(root_dir / "scripts" / "viz.py"), run_name="__main__")

    assert excinfo.value.code == 0
    assert calls == [report_path]
