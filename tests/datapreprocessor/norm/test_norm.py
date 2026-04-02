from pathlib import Path
from io import StringIO

from datasets import load_dataset

from data_preprocessor import NormConfig
from data_preprocessor.norm import NormReport, changes, norm_examples


def test_norm_report_matches_expected():
    root_dir = Path(__file__).resolve().parents[3]
    data_file = root_dir / "tests" / "data" / "testdata_de_en_1000.jsonl"
    report = NormReport.from_path(root_dir / "norm_report.txt")
    ds = load_dataset("json", data_files=str(data_file), split="train")
    it = norm_examples(
        ds,
        NormConfig(
            changes=changes(
                [
                    "strip_edges",
                    "remove_control_chars",
                    "collapse_whitespace",
                    "normalize_unicode_quotes",
                ]
            )
        ),
        report,
    )

    try:
        for ex in it:
            pass
    finally:
        report.close()
        actual_report = root_dir / "norm_report.txt"
        expected_report = root_dir / "tests" / "expected" / "norm" / "norm_report.txt"
        assert actual_report.read_text(encoding="utf-8") == expected_report.read_text(
            encoding="utf-8"
        )


def test_norm_preserves_id_field():
    ds = [{"id": 7, "translation": {"de": "  Hallo  ", "en": "  Hello  "}}]
    out = list(norm_examples(ds))

    assert out[0]["id"] == 7
    assert out[0]["translation"] == {"de": "  Hallo  ", "en": "  Hello  "}


def test_norm_report_is_example_based_and_language_split():
    out = StringIO()
    report = NormReport(out)
    ds = [{"translation": {"de": "  Hallo   Welt  ", "en": "  Hello  "}}]
    list(norm_examples(ds, NormConfig(changes=changes(["strip_edges", "collapse_whitespace"])), report))

    assert out.getvalue() == (
        "{'seq_no': 1, 'de_norm_changes': ['strip_edges', 'collapse_whitespace'], "
        "'en_norm_changes': ['strip_edges']}\n"
    )
