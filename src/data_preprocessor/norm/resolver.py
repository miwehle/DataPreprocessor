from data_preprocessor.shared import resolve_named_callables

from . import changes as change_module


def changes(yaml_change_seq):
    return resolve_named_callables(yaml_change_seq, change_module, kind="change")
