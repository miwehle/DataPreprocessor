from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

try:
    from . import plot_utils as pu
except ImportError:
    import plot_utils as pu


def _count_norm_changes(records: list[dict]) -> tuple[Counter, Counter]:
    de_counts: Counter = Counter()
    en_counts: Counter = Counter()
    for record in records:
        de_counts.update(record.get("de_norm_changes", []))
        en_counts.update(record.get("en_norm_changes", []))
    return de_counts, en_counts


def plot_norm_counts(report_path: str | Path):
    records = pu.load_report_records(report_path)
    de_counts, en_counts = _count_norm_changes(records)
    norm_changes = sorted(
        set(de_counts) | set(en_counts),
        key=lambda change: de_counts.get(change, 0) + en_counts.get(change, 0),
        reverse=True,
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    pu.plot_grouped_category_counts(
        fig,
        ax,
        norm_changes,
        de_counts,
        en_counts,
        "de_norm_changes",
        "en_norm_changes",
        "No norm changes found",
    )
    ax.set_title("Norm Change Counts")
    ax.set_xlabel("Norm change")
    ax.set_ylabel("Count")
    pu.set_coord_display(ax)
    fig.tight_layout()
    pu.attach_adaptive_xtick_labels(fig, ax)
    return fig, ax


def run(report_path: str | Path = "norm_report.txt") -> None:
    plot_norm_counts(report_path)
    plt.show()


def main() -> None:
    run("../artifacts/datasets/iwslt2017_iwslt2017-de-en_train_staging (3)/norm_report.txt")


if __name__ == "__main__":
    main()
