#!/usr/bin/env python3
"""Evaluate whether retrieval returns expected sources for representative queries."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("OMP_NUM_THREADS", "1")

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import Settings  # noqa: E402
from app.db.mongo import create_mongo_client  # noqa: E402
from app.services.retrieval_service import RetrievalService  # noqa: E402


async def evaluate(cases_path: Path, settings: Settings) -> int:
    contents = await asyncio.to_thread(cases_path.read_text, encoding="utf-8")
    cases = json.loads(contents)
    client = create_mongo_client(settings)
    service = RetrievalService(
        database=client[settings.mongodb_database],
        index_path=settings.faiss_index_path,
        metadata_path=settings.faiss_metadata_path,
        embedding_model=settings.embedding_model,
        embedding_device=settings.embedding_device,
        default_top_k=settings.retrieval_top_k,
        candidate_multiplier=settings.retrieval_candidate_multiplier,
        min_score=settings.retrieval_min_score,
        semantic_weight=settings.retrieval_semantic_weight,
    )
    passed = 0
    try:
        for case in cases:
            results = await service.search(case["question"])
            files = {result.source_file for result in results}
            if case["supported"]:
                ok = bool(files.intersection(case["expected_sources"]))
            else:
                ok = not results
            passed += ok
            status = "PASS" if ok else "FAIL"
            print(f"{status}: {case['question']}")
            print(f"  returned: {', '.join(sorted(files)) or '(none)'}")
    finally:
        await client.close()

    total = len(cases)
    print(f"\n{passed}/{total} cases passed ({passed / total:.0%})")
    return 0 if passed == total else 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cases",
        type=Path,
        default=BACKEND_DIR / "evaluation/retrieval_cases.json",
    )
    args = parser.parse_args()
    raise SystemExit(asyncio.run(evaluate(args.cases, Settings())))


if __name__ == "__main__":
    main()
