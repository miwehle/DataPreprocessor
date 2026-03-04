from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.io import dataset_path
from common.ops import download


def main() -> int:
    return download(
        dataset="Helsinki-NLP/europarl",
        config="de-en",
        split="train",
        output=dataset_path("europarl", "raw", "europarl_de-en_train.jsonl"),
        max_rows=None,
    )


if __name__ == "__main__":
    raise SystemExit(main())

