"""Small async facade for mongomock used by the PyMongo Async test suite."""

from collections.abc import AsyncIterator
from typing import Any

import mongomock


class AsyncMongoMockCursor:
    def __init__(self, cursor: Any) -> None:
        self._cursor = cursor

    def sort(self, *args: Any, **kwargs: Any) -> "AsyncMongoMockCursor":
        self._cursor = self._cursor.sort(*args, **kwargs)
        return self

    def skip(self, count: int) -> "AsyncMongoMockCursor":
        self._cursor = self._cursor.skip(count)
        return self

    def limit(self, count: int) -> "AsyncMongoMockCursor":
        self._cursor = self._cursor.limit(count)
        return self

    async def to_list(self, length: int | None = None) -> list[dict[str, Any]]:
        documents = list(self._cursor)
        return documents if length is None else documents[:length]

    async def _iterate(self) -> AsyncIterator[dict[str, Any]]:
        for document in self._cursor:
            yield document

    def __aiter__(self) -> AsyncIterator[dict[str, Any]]:
        return self._iterate()


class AsyncMongoMockCollection:
    def __init__(self, collection: Any) -> None:
        self._collection = collection

    async def create_index(self, *args: Any, **kwargs: Any) -> Any:
        return self._collection.create_index(*args, **kwargs)

    async def update_one(self, *args: Any, **kwargs: Any) -> Any:
        return self._collection.update_one(*args, **kwargs)

    async def insert_many(self, *args: Any, **kwargs: Any) -> Any:
        return self._collection.insert_many(*args, **kwargs)

    async def count_documents(self, *args: Any, **kwargs: Any) -> int:
        return self._collection.count_documents(*args, **kwargs)

    async def bulk_write(self, *args: Any, **kwargs: Any) -> Any:
        return self._collection.bulk_write(*args, **kwargs)

    def find(self, *args: Any, **kwargs: Any) -> AsyncMongoMockCursor:
        return AsyncMongoMockCursor(self._collection.find(*args, **kwargs))

    async def aggregate(self, *args: Any, **kwargs: Any) -> AsyncMongoMockCursor:
        return AsyncMongoMockCursor(self._collection.aggregate(*args, **kwargs))


class AsyncMongoMockDatabase:
    def __init__(self, database: Any) -> None:
        self._database = database

    def __getitem__(self, name: str) -> AsyncMongoMockCollection:
        return AsyncMongoMockCollection(self._database[name])

    def __getattr__(self, name: str) -> AsyncMongoMockCollection:
        return self[name]

    async def command(self, *args: Any, **kwargs: Any) -> Any:
        return self._database.command(*args, **kwargs)


class AsyncMongoMockClient:
    def __init__(self) -> None:
        self._client = mongomock.MongoClient()

    def __getitem__(self, name: str) -> AsyncMongoMockDatabase:
        return AsyncMongoMockDatabase(self._client[name])

    def __getattr__(self, name: str) -> AsyncMongoMockDatabase:
        return self[name]
