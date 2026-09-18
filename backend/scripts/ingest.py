#!/usr/bin/env python3
"""Ingest local Markdown documentation into MongoDB and a persistent FAISS index."""

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from pymongo import UpdateOne

# Conservative defaults avoid native thread conflicts between Torch and FAISS,
# especially on Intel macOS. Explicit shell environment variables still win.
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("OMP_NUM_THREADS", "1")

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import Settings  # noqa: E402
from app.db.mongo import create_indexes, create_mongo_client  # noqa: E402

HEADER_PATTERN = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Chunk:
    content_hash: str
    chunk_id: str
    chunk_text: str
    source_file: str
    section_title: str
    doc_type: str


def infer_doc_type(path: Path) -> str:
    lowered = "/".join(path.parts).lower()
    if "fastapi" in lowered:
        return "fastapi"
    if "mongo" in lowered or "pymongo" in lowered or "motor" in lowered:
        return "mongodb"
    raise ValueError(
        f"Cannot infer doc_type for {path}; place it under a "
        "fastapi/ or mongodb/ folder"
    )


def sections(markdown: str, fallback_title: str) -> list[tuple[str, str]]:
    matches = list(HEADER_PATTERN.finditer(markdown))
    if not matches:
        return [(fallback_title, markdown.strip())]
    result: list[tuple[str, str]] = []
    hierarchy: dict[int, str] = {}
    preamble = markdown[: matches[0].start()].strip()
    if preamble:
        result.append((fallback_title, preamble))
    for index, match in enumerate(matches):
        level = len(match.group(1))
        hierarchy[level] = match.group(2).strip()
        for deeper in tuple(key for key in hierarchy if key > level):
            hierarchy.pop(deeper)
        title = " > ".join(hierarchy[key] for key in sorted(hierarchy))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[match.end() : end].strip()
        if body:
            result.append((title, body))
    return result


def token_chunks(
    text: str, model: Any, target_tokens: int = 254, overlap: int = 50
) -> list[str]:
    # Reserve room for special tokens added by the embedding tokenizer.
    model_limit = getattr(model, "max_seq_length", target_tokens)
    tokenizer_limit = getattr(model.tokenizer, "model_max_length", target_tokens)
    max_sequence_length = min(target_tokens, model_limit, tokenizer_limit)
    target_tokens = max(1, max_sequence_length - 2)
    overlap = min(overlap, target_tokens - 1)
    token_ids = model.tokenizer.encode(text, add_special_tokens=False)
    if not token_ids:
        return []
    chunks = []
    start = 0
    while start < len(token_ids):
        end = min(start + target_tokens, len(token_ids))
        chunks.append(model.tokenizer.decode(token_ids[start:end]).strip())
        if end == len(token_ids):
            break
        start = max(end - overlap, start + 1)
    return chunks


def build_chunks(raw_dir: Path, model: Any, target_tokens: int = 254) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(raw_dir.rglob("*.md")):
        relative_path = path.relative_to(raw_dir)
        doc_type = infer_doc_type(relative_path)
        markdown = path.read_text(encoding="utf-8")
        for title, body in sections(markdown, path.stem):
            for chunk_text in token_chunks(body, model, target_tokens=target_tokens):
                identity = f"{relative_path}\0{title}\0{chunk_text}"
                content_hash = hashlib.sha256(identity.encode()).hexdigest()
                chunks.append(
                    Chunk(
                        content_hash=content_hash,
                        chunk_id=content_hash[:16],
                        chunk_text=chunk_text,
                        source_file=str(relative_path),
                        section_title=title,
                        doc_type=doc_type,
                    )
                )
    return chunks


async def ingest(raw_dir: Path, settings: Settings) -> int:
    from sentence_transformers import SentenceTransformer

    native_threads = max(1, int(os.environ["OMP_NUM_THREADS"]))
    faiss.omp_set_num_threads(native_threads)

    model = await asyncio.to_thread(
        SentenceTransformer,
        settings.embedding_model,
        device=settings.embedding_device,
    )
    chunks = await asyncio.to_thread(
        build_chunks, raw_dir, model, target_tokens=settings.embedding_max_tokens
    )
    if not chunks:
        raise RuntimeError(f"No Markdown chunks found under {raw_dir}")

    texts = [chunk.chunk_text for chunk in chunks]
    vectors = await asyncio.to_thread(
        model.encode,
        texts,
        batch_size=settings.embedding_batch_size,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True,
    )
    vectors = np.asarray(vectors, dtype="float32")
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    client = create_mongo_client(settings)
    database = client[settings.mongodb_database]
    try:
        await create_indexes(database)
        operations = [
            UpdateOne(
                {"content_hash": chunk.content_hash},
                {"$set": chunk.__dict__},
                upsert=True,
            )
            for chunk in chunks
        ]
        await database.documents.bulk_write(operations, ordered=False)
    finally:
        await client.close()

    settings.faiss_index_path.parent.mkdir(parents=True, exist_ok=True)
    settings.faiss_metadata_path.parent.mkdir(parents=True, exist_ok=True)
    await asyncio.to_thread(faiss.write_index, index, str(settings.faiss_index_path))
    settings.faiss_metadata_path.write_text(
        json.dumps(
            {
                "embedding_model": settings.embedding_model,
                "content_hashes": [chunk.content_hash for chunk in chunks],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    count = asyncio.run(ingest(args.raw_dir, Settings()))
    print(f"Indexed {count} chunks")


if __name__ == "__main__":
    main()
