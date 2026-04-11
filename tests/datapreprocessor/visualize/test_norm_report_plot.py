import matplotlib

matplotlib.use("Agg")

from pathlib import Path
from uuid import uuid4

from data_preprocessor.visualize.norm_report_plot import plot_norm_counts


def test_plot_norm_counts_returns_axis_with_language_split_legend() -> None:
    root_dir = Path(__file__).resolve().parents[3]
    path = root_dir / ".local_tmp" / "tests" / "visualize" / f"norms_{uuid4().hex}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "{'de_norm_changes': ['strip_edges'], 'en_norm_changes': ['collapse_whitespace']}\n", encoding="utf-8"
    )
    try:
        _, ax = plot_norm_counts(path)
    finally:
        path.unlink(missing_ok=True)
    assert [text.get_text() for text in ax.get_legend().get_texts()] == ["de_norm_changes", "en_norm_changes"]
    assert len(ax.patches) > 0
