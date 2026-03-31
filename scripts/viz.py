"""Open staging visualizations from the command line."""

from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_preprocessor.visualize import flaws, norms, pairs, token_pairs


def _resolve_input_path(staging_path: Path, mode: str) -> Path:
    if mode in {"-flaws", "-norm"}:
        path = staging_path / {"-flaws": "flaw_report.txt", "-norm": "norm_report.txt"}[mode]
        if path.is_file():
            return path
        raise FileNotFoundError(f"Missing {path.name} in {staging_path}")

    suffix = "_raw.jsonl" if mode == "-pairs" else "_tokenized.jsonl"
    matches = sorted(staging_path.glob(f"*{suffix}"))
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise FileNotFoundError(f"No file ending with {suffix} in {staging_path}")
    raise ValueError(
        f"Expected one file ending with {suffix} in {staging_path}, found {len(matches)}"
    )


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in {"-flaws", "-norm", "-pairs", "-token_pairs"}:
        print("Usage: viz -flaws|-norm|-pairs|-token_pairs <staging-path>")
        return 1

    mode, staging_path = sys.argv[1], Path(sys.argv[2])
    runners = {"-flaws": flaws, "-norm": norms, "-pairs": pairs, "-token_pairs": token_pairs}

    try:
        runners[mode](_resolve_input_path(staging_path, mode))
    except Exception as exc:
        print(f"Visualization failed: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
