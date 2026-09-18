from collections.abc import AsyncIterator

import certifi
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import Settings


def create_mongo_client(settings: Settings) -> AsyncMongoClient:
    """Create a client with a trusted CA bundle for TLS-enabled Atlas URIs."""
    if settings.mongodb_uri.startswith("mongodb+srv://"):
        return AsyncMongoClient(
            settings.mongodb_uri,
            tlsCAFile=certifi.where(),
        )
    return AsyncMongoClient(settings.mongodb_uri)


async def create_indexes(database: AsyncDatabase) -> None:
    await database.chat_messages.create_index(
        [("session_id", 1), ("timestamp", -1)], name="session_timestamp"
    )
    await database.documents.create_index("doc_type", name="document_type")
    await database.documents.create_index(
        [("chunk_text", "text")], name="document_text"
    )
    await database.documents.create_index(
        "content_hash", name="document_content_hash", unique=True
    )
    await database.chat_sessions.create_index(
        "updated_at", name="session_updated_at", background=True
    )


async def database_lifespan(settings: Settings) -> AsyncIterator[AsyncMongoClient]:
    client = create_mongo_client(settings)
    try:
        await create_indexes(client[settings.mongodb_database])
        yield client
    finally:
        await client.close()
