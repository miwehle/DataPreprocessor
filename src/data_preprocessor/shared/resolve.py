from functools import partial


def resolve_named_callables(yaml_seq, module, *, kind):
    if yaml_seq is None:
        return None

    resolved = []
    for item in yaml_seq:
        if isinstance(item, str):
            name, kwargs = item, {}
        elif (
            isinstance(item, list | tuple)
            and len(item) == 2
            and isinstance(item[0], str)
            and isinstance(item[1], dict)
        ):
            name, kwargs = item
        else:
            raise ValueError(f"Invalid {kind} config: {item!r}")

        value = getattr(module, name, None)
        if not callable(value):
            raise ValueError(f"Unknown {kind}: {name}")
        resolved.append(partial(value, **kwargs) if kwargs else value)

    return tuple(resolved)
