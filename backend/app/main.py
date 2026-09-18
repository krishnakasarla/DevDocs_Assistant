import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.routes import router as api_router
from app.core.config import get_settings
from app.db.mongo import database_lifespan

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("OMP_NUM_THREADS", "1")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    async for client in database_lifespan(settings):
        app.state.mongo_client = client
        yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
    app.include_router(health_router)
    app.include_router(api_router, prefix=settings.api_v1_prefix, tags=["api"])
    return app


app = create_app()
