from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class DecodeResult:
    text: str
    is_url: bool
    url: str | None = None


def coerce_url(text: str) -> str | None:
    t = text.strip()
    if not t or any(ch.isspace() for ch in t):
        return None

    parsed = urlparse(t)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return t

    if "://" in t:
        return None

    candidate = "https://" + t
    parsed2 = urlparse(candidate)
    if parsed2.scheme in ("http", "https") and parsed2.netloc and "." in parsed2.netloc:
        return candidate

    return None

