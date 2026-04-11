import matplotlib

matplotlib.use("Agg")

from pathlib import Path
from uuid import uuid4

from data_preprocessor.visualize.token_pair_length_hist_plot import load_token_pair_lengths
from data_preprocessor.visualize.token_pair_length_hist_plot import plot_token_pair_length_histogram

_TMP_DIR = Path(__file__).resolve().parents[3] / ".local_tmp" / "tests" / "visualize"


def _local_temp_jsonl(prefix: str, lines: list[str]) -> Path:
    _TMP_DIR.mkdir(parents=True, exist_ok=True)
    path = _TMP_DIR / f"{prefix}_{uuid4().hex}.jsonl"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def test_load_token_pair_lengths_reads_tokenized_translation_pairs() -> None:
    dataset_path = _local_temp_jsonl(
        "token_pair_lengths",
        [
            '{"tokenized_translation": {"de": {"input_ids": [10, 11, 0]}, "en": {"input_ids": [20, 21, 22, 0]}}}',
            '{"tokenized_translation": {"de": {"input_ids": [30, 0]}, "en": {"input_ids": [40, 41, 0]}}}',
            '{"translation": {"de": "Hallo", "en": "Hello"}}',
        ],
    )
    try:
        assert load_token_pair_lengths(dataset_path) == ([3, 2], [4, 3])
    finally:
        dataset_path.unlink(missing_ok=True)


def test_plot_token_pair_length_histogram_sets_token_xlabel() -> None:
    dataset_path = _local_temp_jsonl(
        "token_pair_histogram",
        [
            '{"tokenized_translation": {"de": {"input_ids": [1, 2, 0]}, "en": {"input_ids": [3, 4, 5, 0]}}}',
            '{"tokenized_translation": {"de": {"input_ids": [6, 0]}, "en": {"input_ids": [7, 8, 0]}}}',
        ],
    )
    try:
        _, ax = plot_token_pair_length_histogram(dataset_path, 5)
    finally:
        dataset_path.unlink(missing_ok=True)
    assert ax.get_xlabel() == "Text length (tokens)"
    assert len(ax.patches) > 0


def test_plot_token_pair_length_histogram_forwards_axis_scales() -> None:
    dataset_path = _local_temp_jsonl(
        "token_pair_scales",
        [
            '{"tokenized_translation": {"de": {"input_ids": [1, 2, 0]}, "en": {"input_ids": [3, 4, 5, 0]}}}',
            '{"tokenized_translation": {"de": {"input_ids": [6, 7, 8, 0]}, "en": {"input_ids": [9, 10, 0]}}}',
        ],
    )
    try:
        _, ax = plot_token_pair_length_histogram(dataset_path, 5, "log", "log", False)
    finally:
        dataset_path.unlink(missing_ok=True)
    assert ax.get_xscale() == "log"
    assert ax.get_yscale() == "log"
