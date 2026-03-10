from __future__ import annotations

from collections.abc import Iterable, Iterator

from datapreprocessor.types import Example


def _normalize_target_ids(
    input_ids: list[int],
    *,
    tgt_bos_id: int | None,
    tgt_eos_id: int | None,
) -> list[int]:
    normalized = [int(x) for x in input_ids]

    if tgt_bos_id is not None:
        if not normalized or normalized[0] != tgt_bos_id:
            normalized = [tgt_bos_id, *normalized]

    if tgt_eos_id is not None:
        if not normalized or normalized[-1] != tgt_eos_id:
            normalized.append(tgt_eos_id)

    return normalized


def to_training_schema(
    ds: Iterable[Example],
    *,
    id_key: str = "id",
    tokenized_key: str = "tokenized_translation",
    src_lang: str = "de",
    tgt_lang: str = "en",
    tgt_bos_id: int | None = None,
    tgt_eos_id: int | None = None,
    include_text: bool = False,
) -> Iterator[Example]:
    """Project tokenized examples to a flat training schema for translation."""
    for ex in ds:
        tokenized = ex[tokenized_key]
        src_ids = [int(x) for x in tokenized[src_lang]["input_ids"]]
        tgt_ids = _normalize_target_ids(
            list(tokenized[tgt_lang]["input_ids"]),
            tgt_bos_id=tgt_bos_id,
            tgt_eos_id=tgt_eos_id,
        )
        out: Example = {
            "id": int(ex[id_key]),
            "src_ids": src_ids,
            "tgt_ids": tgt_ids,
        }
        if include_text:
            translation = ex["translation"]
            out["src_text"] = str(translation[src_lang])
            out["tgt_text"] = str(translation[tgt_lang])
        yield out
