import matplotlib

matplotlib.use("Agg")

from pathlib import Path
from uuid import uuid4

from data_preprocessor.visualize.pair_length_hist_plot import load_pair_lengths
from data_preprocessor.visualize.pair_length_hist_plot import plot_pair_length_histogram


_TMP_DIR = Path(__file__).resolve().parents[3] / ".local_tmp" / "tests" / "visualize"


def _local_temp_jsonl(prefix: str, lines: list[str]) -> Path:
    _TMP_DIR.mkdir(parents=True, exist_ok=True)
    path = _TMP_DIR / f"{prefix}_{uuid4().hex}.jsonl"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def test_load_pair_lengths_reads_translation_pairs() -> None:
    dataset_path = _local_temp_jsonl("pair_lengths", [
        '{"translation": {"de": "Hallo", "en": "Hello"}}',
        '{"translation": {"de": "Welt", "en": "World!"}}',
        '{"foo": "bar"}',
    ])
    try:
        assert load_pair_lengths(dataset_path) == ([5, 4], [5, 6])
    finally:
        dataset_path.unlink(missing_ok=True)


def test_plot_pair_length_histogram_returns_axis_with_two_histograms() -> None:
    dataset_path = _local_temp_jsonl("pair_histogram", [
        '{"translation": {"de": "a", "en": "bb"}}',
        '{"translation": {"de": "ccc", "en": "dddd"}}',
    ])
    try:
        _, ax = plot_pair_length_histogram(dataset_path, 5)
    finally:
        dataset_path.unlink(missing_ok=True)
    assert [text.get_text() for text in ax.get_legend().get_texts()] == ["de", "en"]
    assert len(ax.patches) > 0


def test_plot_pair_length_histogram_accepts_log_scale_on_call() -> None:
    dataset_path = _local_temp_jsonl("pair_log_scale", [
        '{"translation": {"de": "a", "en": "bb"}}',
        '{"translation": {"de": "ccc", "en": "dddd"}}',
    ])
    try:
        _, ax = plot_pair_length_histogram(dataset_path, 5, "linear", "log", False)
    finally:
        dataset_path.unlink(missing_ok=True)
    assert ax.get_yscale() == "log"


def test_plot_pair_length_histogram_supports_all_axis_scale_combinations() -> None:
    dataset_path = _local_temp_jsonl("pair_scales", [
        '{"translation": {"de": "a", "en": "bb"}}',
        '{"translation": {"de": "ccc", "en": "dddd"}}',
        '{"translation": {"de": "eeeee", "en": "ffffff"}}',
    ])
    try:
        for x_scale, y_scale in [("linear", "linear"), ("log", "linear"), ("linear", "log"), ("log", "log")]:
            _, ax = plot_pair_length_histogram(dataset_path, 5, x_scale, y_scale, False)
            assert ax.get_xscale() == x_scale
            assert ax.get_yscale() == y_scale
    finally:
        dataset_path.unlink(missing_ok=True)
