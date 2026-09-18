import asyncio
import json
import re
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from pymongo.asynchronous.database import AsyncDatabase

from app.models.schemas import SourceChunk

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "application",
    "can",
    "create",
    "do",
    "fastapi",
    "how",
    "i",
    "in",
    "is",
    "it",
    "of",
    "the",
    "to",
    "use",
    "using",
    "with",
}


def _tokens(value: str) -> set[str]:
    return {
        token
        for token in TOKEN_PATTERN.findall(value.lower())
        if token not in STOP_WORDS
    }


def lexical_overlap(query: str, document: dict[str, Any]) -> float:
    """Return the fraction of meaningful query terms present in a chunk."""
    query_tokens = _tokens(query)
    if not query_tokens:
        return 0.0
    searchable = " ".join(
        str(document.get(field, ""))
        for field in ("source_file", "section_title", "chunk_text")
    )
    return len(query_tokens & _tokens(searchable)) / len(query_tokens)


def combined_score(
    semantic_score: float,
    lexical_score: float,
    semantic_weight: float,
) -> float:
    return semantic_weight * semantic_score + (1 - semantic_weight) * lexical_score


class RetrievalService:
    def __init__(
        self,
        database: AsyncDatabase,
        index_path: Path,
        metadata_path: Path,
        embedding_model: str,
        embedding_device: str = "cpu",
        default_top_k: int = 5,
        candidate_multiplier: int = 4,
        min_score: float = 0.5,
        semantic_weight: float = 0.65,
    ) -> None:
        self.database = database
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.embedding_model_name = embedding_model
        self.embedding_device = embedding_device
        self.default_top_k = default_top_k
        self.candidate_multiplier = candidate_multiplier
        self.min_score = min_score
        self.semantic_weight = semantic_weight
        self._model: Any | None = None
        self._index: Any | None = None
        self._content_hashes: list[str] = []

    def _load(self) -> None:
        if self._index is not None:
            return
        if not self.index_path.exists() or not self.metadata_path.exists():
            raise FileNotFoundError(
                "FAISS index not found; run backend/scripts/ingest.py"
            )
        self._index = faiss.read_index(str(self.index_path))
        mapping = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        if mapping.get("embedding_model") != self.embedding_model_name:
            raise ValueError("FAISS index uses a different embedding model")
        self._content_hashes = mapping["content_hashes"]
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(
            self.embedding_model_name, device=self.embedding_device
        )

    async def search(self, query: str, top_k: int | None = None) -> list[SourceChunk]:
        await asyncio.to_thread(self._load)
        assert self._model is not None and self._index is not None
        result_count = top_k or self.default_top_k
        k = min(result_count * self.candidate_multiplier, self._index.ntotal)
        if k == 0:
            return []
        vector = await asyncio.to_thread(
            self._model.encode,
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        scores, positions = await asyncio.to_thread(
            self._index.search, np.asarray(vector, dtype="float32"), k
        )
        ranked_hashes = [
            self._content_hashes[position]
            for position in positions[0]
            if 0 <= position < len(self._content_hashes)
        ]
        documents = {
            doc["content_hash"]: doc
            async for doc in self.database.documents.find(
                {"content_hash": {"$in": ranked_hashes}}, {"_id": 0}
            )
        }
        results: list[SourceChunk] = []
        for content_hash, score in zip(ranked_hashes, scores[0], strict=False):
            semantic_score = float(score)
            if semantic_score < self.min_score:
                continue
            if document := documents.get(content_hash):
                score = combined_score(
                    semantic_score,
                    lexical_overlap(query, document),
                    self.semantic_weight,
                )
                results.append(SourceChunk(**document, score=score))
        results.sort(key=lambda source: source.score, reverse=True)
        return results[:result_count]
