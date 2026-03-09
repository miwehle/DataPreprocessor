from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "scripts"))
from ipy import ops


def test_ops_preprocess_calls_stages_in_order(monkeypatch):
    calls: list[tuple[str, dict]] = []

    def fake_dataset_path(dataset: str, stage: str, filename: str) -> Path:
        return Path(f"C:/tmp/{dataset}/{stage}/{filename}")

    def fake_download(**kwargs):
        calls.append(("download", kwargs))

    def fake_norm(**kwargs):
        calls.append(("norm", kwargs))

    def fake_filter(**kwargs):
        calls.append(("filter", kwargs))

    def fake_tokenize(**kwargs):
        calls.append(("tokenize", kwargs))

    def fake_map(**kwargs):
        calls.append(("map", kwargs))

    monkeypatch.setattr(ops, "dataset_path", fake_dataset_path)
    monkeypatch.setattr(ops, "download", fake_download)
    monkeypatch.setattr(ops, "norm", fake_norm)
    monkeypatch.setattr(ops, "filter", fake_filter)
    monkeypatch.setattr(ops, "tokenize", fake_tokenize)
    monkeypatch.setattr(ops, "map", fake_map)

    ops.preprocess(
        download_cfg={"max_records": 123},
        map_cfg={"include_text": True},
    )

    assert [name for name, _ in calls] == ["download", "norm", "filter", "tokenize", "map"]
    assert calls[0][1]["max_records"] == 123
    assert calls[0][1]["include_ids"] is True
    assert calls[-1][1]["include_text"] is True


def test_ops_preprocess_accepts_path_overrides(monkeypatch):
    calls: list[tuple[str, dict]] = []

    def fake_dataset_path(dataset: str, stage: str, filename: str) -> Path:
        return Path(f"C:/tmp/{dataset}/{stage}/{filename}")

    def fake_download(**kwargs):
        calls.append(("download", kwargs))

    def fake_norm(**kwargs):
        calls.append(("norm", kwargs))

    def fake_filter(**kwargs):
        calls.append(("filter", kwargs))

    def fake_tokenize(**kwargs):
        calls.append(("tokenize", kwargs))

    def fake_map(**kwargs):
        calls.append(("map", kwargs))

    monkeypatch.setattr(ops, "dataset_path", fake_dataset_path)
    monkeypatch.setattr(ops, "download", fake_download)
    monkeypatch.setattr(ops, "norm", fake_norm)
    monkeypatch.setattr(ops, "filter", fake_filter)
    monkeypatch.setattr(ops, "tokenize", fake_tokenize)
    monkeypatch.setattr(ops, "map", fake_map)

    ops.preprocess(paths={"map_output": "C:/custom/final.jsonl"})

    assert calls[-1][1]["output_path"] == Path("C:/custom/final.jsonl")


def test_ops_preprocess_derives_filesystem_dataset_name(monkeypatch):
    seen_dataset_names: list[str] = []

    def fake_dataset_path(dataset: str, stage: str, filename: str) -> Path:
        seen_dataset_names.append(dataset)
        return Path(f"C:/tmp/{dataset}/{stage}/{filename}")

    monkeypatch.setattr(ops, "dataset_path", fake_dataset_path)
    monkeypatch.setattr(ops, "download", lambda **kwargs: None)
    monkeypatch.setattr(ops, "norm", lambda **kwargs: None)
    monkeypatch.setattr(ops, "filter", lambda **kwargs: None)
    monkeypatch.setattr(ops, "tokenize", lambda **kwargs: None)
    monkeypatch.setattr(ops, "map", lambda **kwargs: None)

    ops.preprocess(dataset="Org/My-Data Set+V1")

    assert seen_dataset_names
    assert all(name == "My-Data_Set_V1" for name in seen_dataset_names)
