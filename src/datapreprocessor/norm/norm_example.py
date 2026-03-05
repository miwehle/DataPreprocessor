from pathlib import Path
from typing import Any, Callable, Dict, Protocol, TextIO

from . import changes as c

Change = Callable[[str], str]
Example = Dict[str, Any]

CHANGES: list[Change] = [
    c.strip_edges,
    c.remove_control_chars,
    c.collapse_whitespace,
    c.normalize_unicode_quotes,
    c.fix_apostrophe_spacing,
]

def apply_changes(text: str, changes: list[Change] = CHANGES) -> tuple[str, list[str]]:
    change_names: list[str] = []
    current = text
    for change in changes:
        updated = change(current)
        if updated != current:
            change_names.append(change.__name__)
        current = updated
    return current, change_names


class NormReporter(Protocol):
    def note_change(self, before: str, after: str, norm_changes: list[str]) -> None: ...


class NormReport:
    def __init__(self, out: TextIO, *, debug: bool = False):
        self.out = out
        self.debug = debug
        self.seq_no = 0

    @classmethod
    def from_path(cls, path: str | Path = "norm_report.txt", *, debug: bool = False) -> "NormReport":
        return cls(open(path, "w", encoding="utf-8"), debug=debug)

    def note_change(self, before: str, after: str, norm_changes: list[str]) -> None:
        self.seq_no += 1
        if not norm_changes:
            return
        record = {
            "seq_no": self.seq_no,
            "norm_changes": norm_changes,
        }
        if self.debug:
            record["before"] = before
            record["after"] = after
        self.out.write(f"{record}\n")

    def flush(self) -> None:
        self.out.flush()

    def close(self) -> None:
        self.out.close()


def norm_example(
    ex: Example,
    changes: list[Change] = CHANGES,
    norm_reporter: NormReporter | None = None,
) -> Example:
    """Return a normalized copy of one translation example with de/en texts."""
    def norm(s: str) -> str:
        """Normalize text by removing control chars and collapsing whitespace."""
        before = str(s)
        after, norm_changes = apply_changes(before, changes=changes)

        if norm_reporter is not None:
            norm_reporter.note_change(before, after, norm_changes)

        return after

    normalized = dict(ex)
    translation = dict(normalized["translation"])
    translation["de"] = norm(translation["de"])
    translation["en"] = norm(translation["en"])
    normalized["translation"] = translation
    return normalized
