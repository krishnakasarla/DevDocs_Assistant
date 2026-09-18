from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.dependencies import get_database
from app.main import app
from tests.async_mongomock import AsyncMongoMockClient


@pytest.fixture
def database():
    client = AsyncMongoMockClient()
    return client.devdocs_test


@pytest.fixture
async def client(database) -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_database] = lambda: database
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as test_client:
        yield test_client
    app.dependency_overrides.clear()
