from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.asynchronous.database import AsyncDatabase

from app.core.dependencies import SettingsDep, get_database

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(
    database: Annotated[AsyncDatabase, Depends(get_database)],
    settings: SettingsDep,
) -> dict[str, str]:
    try:
        await database.command("ping")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB is unavailable",
        ) from exc
    if (
        not settings.faiss_index_path.is_file()
        or not settings.faiss_metadata_path.is_file()
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="FAISS index is unavailable; run ingestion",
        )
    return {"status": "ready"}
