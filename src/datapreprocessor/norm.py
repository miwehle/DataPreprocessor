import re

_WHITESPACE_RE = re.compile(r"\s+")
_CTRL_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")

def norm(s: str) -> str:
    """ Normalize text by removing control chars and collapsing whitespace. """
    s = str(s).strip()
    s = _CTRL_RE.sub("", s)
    s = _WHITESPACE_RE.sub(" ", s)
    return s
