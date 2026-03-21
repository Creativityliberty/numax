from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class RetrievedChunk:
    source_id: str
    text: str
    score: float


class SimpleRetrievalEngine:
    def __init__(self, documents: list[dict]) -> None:
        self.documents = documents

    def search(self, query: str, top_k: int = 3) -> List[RetrievedChunk]:
        query_terms = {term.lower() for term in query.split() if term.strip()}
        results: list[RetrievedChunk] = []

        for doc in self.documents:
            text = doc["text"]
            text_terms = set(text.lower().split())
            overlap = query_terms.intersection(text_terms)
            score = float(len(overlap))

            if score > 0:
                results.append(
                    RetrievedChunk(
                        source_id=doc["id"],
                        text=text,
                        score=score,
                    )
                )

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]
