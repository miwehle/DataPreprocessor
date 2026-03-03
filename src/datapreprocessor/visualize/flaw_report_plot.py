from __future__ import annotations

import ast
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


def _load_records(report_path: str | Path) -> list[dict]:
    path = Path(report_path)
    records: list[dict] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        record = ast.literal_eval(line)
        if isinstance(record, dict):
            records.append(record)

    return records


def _count_flaws(records: list[dict]) -> tuple[Counter, Counter, Counter]:
    de_counts: Counter = Counter()
    en_counts: Counter = Counter()
    pair_counts: Counter = Counter()

    for record in records:
        de_counts.update(record.get("de_flaws", []))
        en_counts.update(record.get("en_flaws", []))
        pair_counts.update(record.get("pair_flaws", []))

    return de_counts, en_counts, pair_counts


def plot_flaw_counts(report_path: str | Path):
    """
    Build a grouped bar chart for flaw counts split by
    de_flaws, en_flaws and pair_flaws.
    """
    records = _load_records(report_path)
    de_counts, en_counts, pair_counts = _count_flaws(records)

    all_flaws = sorted(
        set(de_counts.keys()) | set(en_counts.keys()) | set(pair_counts.keys()),
        key=lambda flaw: de_counts.get(flaw, 0) + en_counts.get(flaw, 0) + pair_counts.get(flaw, 0),
        reverse=True,
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    if not all_flaws:
        ax.text(0.5, 0.5, "No flaws found", ha="center", va="center")
        ax.set_axis_off()
        return fig, ax

    x = list(range(len(all_flaws)))
    width = 0.25

    ax.bar([i - width for i in x], [de_counts.get(f, 0) for f in all_flaws], width=width, label="de_flaws")
    ax.bar(x, [en_counts.get(f, 0) for f in all_flaws], width=width, label="en_flaws")
    ax.bar([i + width for i in x], [pair_counts.get(f, 0) for f in all_flaws], width=width, label="pair_flaws")

    ax.set_title("Flaw Counts by Category")
    ax.set_xlabel("Flaw")
    ax.set_ylabel("Count")
    ax.set_xticks(x)
    ax.set_xticklabels(all_flaws, rotation=45, ha="right")
    ax.legend()
    fig.tight_layout()
    return fig, ax

