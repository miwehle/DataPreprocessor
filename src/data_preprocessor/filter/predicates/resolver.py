from functools import partial

from . import text_pair_predicates, text_predicates


def _resolve(yaml_pred_seq, module):
    if yaml_pred_seq is None:
        return None

    resolved = []
    for item in yaml_pred_seq:
        if isinstance(item, str):
            name, kwargs = item, {}
        elif (isinstance(item, list | tuple) and len(item) == 2 and
              isinstance(item[0], str) and isinstance(item[1], dict)):
            name, kwargs = item
        else:
            raise ValueError(f"Invalid predicate config: {item!r}")

        pred = getattr(module, name, None)
        if not callable(pred):
            raise ValueError(f"Unknown predicate: {name}")
        resolved.append(partial(pred, **kwargs) if kwargs else pred)

    return tuple(resolved)


def predicates(yaml_pred_seq):
    return _resolve(yaml_pred_seq, text_predicates)


def pair_predicates(yaml_pair_pred_seq):
    return _resolve(yaml_pair_pred_seq, text_pair_predicates)
