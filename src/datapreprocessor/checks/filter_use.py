# ANWENDUNG

from typing import TextIO

from datasets import load_dataset

if __package__ in (None, ""):
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from datapreprocessor.checks.filter import filtered_examples, Example
    from datapreprocessor.checks.check import check, check_pair, TEXT_FLAWS, TEXT_PAIR_FLAWS
else:
    from .filter import filtered_examples, Example
    from .check import check, check_pair, TEXT_FLAWS, TEXT_PAIR_FLAWS

class FlawReport:
    def __init__(self, out: TextIO):
        self.out = out
        self.seq_no = 0

    def note_flaws(self, de_flaws, en_flaws, pair_flaws):
        self.seq_no += 1
        record = {
            "seq_no": self.seq_no,
            "de_flaws": de_flaws,
            "en_flaws": en_flaws,
            "pair_flaws": pair_flaws,
        }

        self.out.write(f"{record}\n")

        return record

report_out: TextIO = open("flaw_report.log", "w", encoding="utf-8")
report = FlawReport(report_out)

def is_flawless(ex: Example):
    # dein Filterkriterium (hier Dummy)

    de = ex["translation"]["de"]
    en = ex["translation"]["en"]

    de_flaws = check(de, TEXT_FLAWS)
    en_flaws = check(en, TEXT_FLAWS)
    pair_flaws = check_pair(de, en, TEXT_PAIR_FLAWS)

    report.note_flaws(de_flaws, en_flaws, pair_flaws)

    return de_flaws == [] and en_flaws == [] and pair_flaws == []



ds = load_dataset("json", data_files="data/testdata_de_en_100.jsonl", split="train")
#ds = load_dataset("Helsinki-NLP/europarl", "de-en", split="train", streaming=True)
it = filtered_examples(ds, is_flawless)

try:
    for ex in it:
        pass
finally:
    report_out.close()


"""
try:
    i = 0
    for ex in it:
        if i >= 10:
            break
        pass
        i=i+1
finally:
    report_out.close()
"""

"""
# 1) Streaming-Quelle (große Daten): iteriert ohne alles in RAM
ds = load_dataset("Helsinki-NLP/europarl", "de-en", split="train", streaming=True)

# A) nur durchstreamen (z.B. Tokenizer)
it = stream_or_save(ds, keep)
for ex in it:
    # tokenizer(ex["translation"]["de"], ...)
    pass

# B) durchstreamen UND nebenbei JSONL schreiben
it = stream_or_save(ds, keep, out_jsonl="filtered/europarl_de_en.jsonl")
for ex in it:
    pass

# C) als HF-Dataset speichern (materialisiert komplett)
it = stream_or_save(ds, keep)
save_to_disk_from_iter(it, "filtered/europarl_de_en_saved")
"""
