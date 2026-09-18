from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, Query
from pymongo.asynchronous.database import AsyncDatabase

from app.core.dependencies import get_database, get_qa_service
from app.models.schemas import (
    ChatMessage,
    PaginatedHistory,
    QueryRequest,
    QueryResponse,
    SessionSummary,
    StatsResponse,
)
from app.services.qa_service import QAService

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(
    payload: QueryRequest,
    database: Annotated[AsyncDatabase, Depends(get_database)],
    qa_service: Annotated[QAService, Depends(get_qa_service)],
) -> QueryResponse:
    session_id = payload.session_id or str(uuid4())
    now = datetime.now(UTC)
    answer, sources = await qa_service.answer(payload.question)
    serialized_sources = [source.model_dump() for source in sources]

    await database.chat_sessions.update_one(
        {"session_id": session_id},
        {
            "$setOnInsert": {
                "session_id": session_id,
                "title": payload.question[:80],
                "created_at": now,
            },
            "$set": {"updated_at": now},
            "$inc": {"message_count": 2},
        },
        upsert=True,
    )
    await database.chat_messages.insert_many(
        [
            {
                "session_id": session_id,
                "role": "user",
                "content": payload.question,
                "timestamp": now,
                "sources": [],
            },
            {
                "session_id": session_id,
                "role": "assistant",
                "content": answer,
                "timestamp": now,
                "sources": serialized_sources,
            },
        ]
    )
    return QueryResponse(answer=answer, sources=sources, session_id=session_id)


@router.get("/sessions/{session_id}/history", response_model=PaginatedHistory)
async def session_history(
    session_id: str,
    database: Annotated[AsyncDatabase, Depends(get_database)],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> PaginatedHistory:
    criteria = {"session_id": session_id}
    total = await database.chat_messages.count_documents(criteria)
    cursor = (
        database.chat_messages.find(criteria)
        .sort([("timestamp", 1), ("_id", 1)])
        .skip((page - 1) * page_size)
        .limit(page_size)
    )
    items = []
    async for message in cursor:
        message["id"] = str(message.pop("_id"))
        items.append(ChatMessage.model_validate(message))
    return PaginatedHistory(items=items, page=page, page_size=page_size, total=total)


@router.get("/sessions", response_model=list[SessionSummary])
async def list_sessions(
    database: Annotated[AsyncDatabase, Depends(get_database)],
    limit: int = Query(default=25, ge=1, le=100),
) -> list[SessionSummary]:
    cursor = (
        database.chat_sessions.find({}, {"_id": 0}).sort("updated_at", -1).limit(limit)
    )
    return [SessionSummary.model_validate(session) async for session in cursor]


@router.get("/stats", response_model=StatsResponse)
async def stats(
    database: Annotated[AsyncDatabase, Depends(get_database)],
) -> StatsResponse:
    pipeline = [
        {
            "$facet": {
                "most_queried_sections": [
                    {"$match": {"role": "assistant"}},
                    {"$unwind": "$sources"},
                    {
                        "$group": {
                            "_id": {
                                "source_file": "$sources.source_file",
                                "section_title": "$sources.section_title",
                            },
                            "count": {"$sum": 1},
                        }
                    },
                    {"$sort": {"count": -1}},
                    {"$limit": 10},
                    {
                        "$project": {
                            "_id": 0,
                            "source_file": "$_id.source_file",
                            "section_title": "$_id.section_title",
                            "count": 1,
                        }
                    },
                ],
                "query_volume_over_time": [
                    {"$match": {"role": "user"}},
                    {
                        "$group": {
                            "_id": {
                                "$dateToString": {
                                    "format": "%Y-%m-%d",
                                    "date": "$timestamp",
                                }
                            },
                            "count": {"$sum": 1},
                        }
                    },
                    {"$sort": {"_id": 1}},
                    {"$project": {"_id": 0, "date": "$_id", "count": 1}},
                ],
                "source_average": [
                    {"$match": {"role": "assistant"}},
                    {
                        "$group": {
                            "_id": None,
                            "value": {"$avg": {"$size": {"$ifNull": ["$sources", []]}}},
                        }
                    },
                ],
            }
        }
    ]
    cursor = await database.chat_messages.aggregate(pipeline)
    facets = (await cursor.to_list(length=1))[0]
    source_average = facets["source_average"]
    return StatsResponse(
        most_queried_sections=facets["most_queried_sections"],
        query_volume_over_time=facets["query_volume_over_time"],
        average_sources_per_answer=(
            source_average[0]["value"] if source_average else 0
        ),
    )
