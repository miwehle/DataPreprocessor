from __future__ import annotations


def build_dataset_meta(
    *,
    tokenizer_model_name: str,
    src_lang: str,
    tgt_lang: str,
    id_field: str,
    src_field: str = "src_ids",
    tgt_field: str = "tgt_ids",
    tgt_bos_id: int,
    tgt_eos_id: int,
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "tokenizer_model_name": tokenizer_model_name,
        "src_lang": src_lang,
        "tgt_lang": tgt_lang,
        "id_field": id_field,
        "src_field": src_field,
        "tgt_field": tgt_field,
        "tgt_bos_id": tgt_bos_id,
        "tgt_eos_id": tgt_eos_id,
    }
