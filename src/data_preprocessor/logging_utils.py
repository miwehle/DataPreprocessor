from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from time import perf_counter
from typing import Any


def log_calls(log_path: Callable[[], Path]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorate(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__module__)
            if not logger.handlers:
                path = log_path()
                path.parent.mkdir(parents=True, exist_ok=True)
                handler = logging.FileHandler(path, encoding="utf-8")
                handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
                handler.formatter.default_msec_format = "%s,%03d"
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
                logger.propagate = False
            logger.info("Start %s", func.__name__)
            started = perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                logger.info("Finished %s in %.3fs", func.__name__, perf_counter() - started)

        return wrapper

    return decorate
