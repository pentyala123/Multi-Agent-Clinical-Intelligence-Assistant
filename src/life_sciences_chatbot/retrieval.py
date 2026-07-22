from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RetrievedDocument:
    title: str
    source: str
    content: str


class SyntheticKnowledgeBase:
    """Small local retriever that keeps the public demonstration deterministic."""

    def __init__(self, path: str | Path) -> None:
        with Path(path).open(encoding="utf-8") as handle:
            self.documents = [RetrievedDocument(**item) for item in json.load(handle)["documents"]]

    def search(self, query: str, *, domain: str, limit: int = 3) -> list[RetrievedDocument]:
        terms = set(re.findall(r"[a-z0-9]+", query.casefold()))

        def score(document: RetrievedDocument) -> int:
            text = f"{document.title} {document.content}".casefold()
            return sum(term in text for term in terms) + int(domain.replace("_", " ") in text)

        ranked = sorted(self.documents, key=score, reverse=True)
        return [document for document in ranked if score(document) > 0][:limit]
