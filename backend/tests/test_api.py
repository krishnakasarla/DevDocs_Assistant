from datetime import UTC, datetime, timedelta

import pytest

from app.core.dependencies import get_qa_service
from app.main import app
from app.models.schemas import SourceChunk


class FakeQAService:
    async def answer(self, question: str):
        return (
            f"Grounded answer to: {question}",
            [
                SourceChunk(
                    chunk_id="abc123",
                    source_file="fastapi/tutorial/body.md",
                    section_title="Request body",
                    doc_type="fastapi",
                    chunk_text="Declare request bodies with Pydantic models.",
                    score=0.91,
                )
            ],
        )


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_query_happy_path(client, database):
    app.dependency_overrides[get_qa_service] = lambda: FakeQAService()
    response = await client.post(
        "/api/v1/query", json={"session_id": "session-1", "question": "Bodies?"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == "session-1"
    assert body["sources"][0]["section_title"] == "Request body"
    assert (
        await database.chat_messages.count_documents({"session_id": "session-1"}) == 2
    )


@pytest.mark.asyncio
async def test_history_pagination(client, database):
    now = datetime.now(UTC)
    await database.chat_messages.insert_many(
        [
            {
                "session_id": "paged",
                "role": "user",
                "content": f"message-{index}",
                "timestamp": now + timedelta(seconds=index),
                "sources": [],
            }
            for index in range(5)
        ]
    )

    response = await client.get(
        "/api/v1/sessions/paged/history", params={"page": 2, "page_size": 2}
    )

    assert response.status_code == 200
    assert response.json()["total"] == 5
    assert [item["content"] for item in response.json()["items"]] == [
        "message-2",
        "message-3",
    ]


@pytest.mark.asyncio
async def test_stats_uses_message_data(client, database):
    now = datetime(2026, 1, 2, tzinfo=UTC)
    source = {
        "chunk_id": "one",
        "source_file": "mongodb/indexes.md",
        "section_title": "Indexes",
        "doc_type": "mongodb",
        "chunk_text": "Indexes improve common queries.",
        "score": 0.88,
    }
    await database.chat_messages.insert_many(
        [
            {
                "session_id": "stats",
                "role": "user",
                "content": "What is an index?",
                "timestamp": now,
                "sources": [],
            },
            {
                "session_id": "stats",
                "role": "assistant",
                "content": "An index...",
                "timestamp": now,
                "sources": [source],
            },
        ]
    )

    response = await client.get("/api/v1/stats")

    assert response.status_code == 200
    body = response.json()
    assert body["most_queried_sections"][0]["section_title"] == "Indexes"
    assert body["query_volume_over_time"] == [{"date": "2026-01-02", "count": 1}]
    assert body["average_sources_per_answer"] == 1.0
