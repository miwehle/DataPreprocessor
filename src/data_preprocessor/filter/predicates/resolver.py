from data_preprocessor.shared import resolve_named_callables

from . import text_pair_predicates, text_predicates


def predicates(yaml_pred_seq):
    return resolve_named_callables(yaml_pred_seq, text_predicates, kind="predicate")


def pair_predicates(yaml_pair_pred_seq):
    return resolve_named_callables(yaml_pair_pred_seq, text_pair_predicates, kind="predicate")
