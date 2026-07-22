from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ChatRequestData:
    query: str
    session_id: str | None = None


@dataclass(frozen=True)
class ChatResult:
    response: str
    routed_to: str
    sources: list[str]
    session_id: str | None
    disclaimer: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
