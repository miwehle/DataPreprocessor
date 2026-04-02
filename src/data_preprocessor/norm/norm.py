from __future__ import annotations

from typing import Iterable, Iterator

from data_preprocessor.shared import NormConfig

from .changes import Change
from .norm_example import Example, NormReporter, norm_example


def norm_examples(
    ds: Iterable[Example],
    config: NormConfig | None = None,
    norm_reporter: NormReporter | None = None,
) -> Iterator[Example]:
    """Yield normalized examples from an input iterable."""
    changes: Iterable[Change] = () if config is None else config.changes or ()
    for ex in ds:
        yield norm_example(ex, changes=changes, norm_reporter=norm_reporter)
