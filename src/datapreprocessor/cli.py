from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from datasets import load_dataset

from datapreprocessor.filter.filter import Example, filter_examples
from datapreprocessor.filter.keep import FlawReport, keep
from datapreprocessor.norm import NormReport, norm_examples


def _load_jsonl(path: str):
    return load_dataset("json", data_files=str(path), split="train")


def _write_jsonl(examples: Iterable[Example], output_path: str) -> None:
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")


def _run_norm(args: argparse.Namespace) -> int:
    ds = _load_jsonl(args.input)
    report = NormReport.from_path(args.norm_report, debug=args.norm_debug)
    try:
        it = norm_examples(ds, norm_reporter=report)
        _write_jsonl(it, args.output)
    finally:
        report.close()
    return 0


def _run_filter(args: argparse.Namespace) -> int:
    ds = _load_jsonl(args.input)
    report = FlawReport.from_path(args.flaw_report)
    try:
        it = filter_examples(ds, lambda ex: keep(ex, flaw_reporter=report))
        _write_jsonl(it, args.output)
    finally:
        report.close()
    return 0


def _run_pipeline(args: argparse.Namespace) -> int:
    ds = _load_jsonl(args.input)
    norm_report = NormReport.from_path(args.norm_report, debug=args.norm_debug)
    flaw_report = FlawReport.from_path(args.flaw_report)
    try:
        it = norm_examples(ds, norm_reporter=norm_report)
        it = filter_examples(it, lambda ex: keep(ex, flaw_reporter=flaw_report))
        _write_jsonl(it, args.output)
    finally:
        norm_report.close()
        flaw_report.close()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="datapreprocessor", description="Normalize and filter translation JSONL data.")
    sub = parser.add_subparsers(dest="command", required=True)

    norm_parser = sub.add_parser("norm", help="Normalize input examples and write JSONL output.")
    norm_parser.add_argument("--input", required=True, help="Path to input JSONL file.")
    norm_parser.add_argument("--output", required=True, help="Path to output JSONL file.")
    norm_parser.add_argument("--norm-report", default="norm_report.txt", help="Path to norm report output file.")
    norm_parser.add_argument("--norm-debug", action="store_true", help="Include before/after text in norm report.")
    norm_parser.set_defaults(func=_run_norm)

    filter_parser = sub.add_parser("filter", help="Filter input examples and write JSONL output.")
    filter_parser.add_argument("--input", required=True, help="Path to input JSONL file.")
    filter_parser.add_argument("--output", required=True, help="Path to output JSONL file.")
    filter_parser.add_argument("--flaw-report", default="flaw_report.txt", help="Path to flaw report output file.")
    filter_parser.set_defaults(func=_run_filter)

    pipe_parser = sub.add_parser("pipeline", help="Run normalize -> filter and write JSONL output.")
    pipe_parser.add_argument("--input", required=True, help="Path to input JSONL file.")
    pipe_parser.add_argument("--output", required=True, help="Path to output JSONL file.")
    pipe_parser.add_argument("--norm-report", default="norm_report.txt", help="Path to norm report output file.")
    pipe_parser.add_argument("--norm-debug", action="store_true", help="Include before/after text in norm report.")
    pipe_parser.add_argument("--flaw-report", default="flaw_report.txt", help="Path to flaw report output file.")
    pipe_parser.set_defaults(func=_run_pipeline)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

