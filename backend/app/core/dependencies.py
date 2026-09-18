from typing import Annotated

from fastapi import Depends, Request
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import Settings, get_settings
from app.llm.base import LLMProvider
from app.llm.providers import GroqProvider, OllamaProvider
from app.services.qa_service import QAService
from app.services.retrieval_service import RetrievalService

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_database(request: Request, settings: SettingsDep) -> AsyncDatabase:
    return request.app.state.mongo_client[settings.mongodb_database]


def get_llm_provider(settings: SettingsDep) -> LLMProvider:
    if settings.llm_provider == "groq":
        return GroqProvider(
            api_key=settings.groq_api_key or "",
            model=settings.groq_model,
            base_url=settings.groq_base_url,
            timeout=settings.llm_timeout_seconds,
        )
    return OllamaProvider(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        timeout=settings.llm_timeout_seconds,
    )


def get_retrieval_service(
    request: Request,
    database: Annotated[AsyncDatabase, Depends(get_database)],
    settings: SettingsDep,
) -> RetrievalService:
    if service := getattr(request.app.state, "retrieval_service", None):
        return service
    service = RetrievalService(
        database=database,
        index_path=settings.faiss_index_path,
        metadata_path=settings.faiss_metadata_path,
        embedding_model=settings.embedding_model,
        embedding_device=settings.embedding_device,
        default_top_k=settings.retrieval_top_k,
        candidate_multiplier=settings.retrieval_candidate_multiplier,
        min_score=settings.retrieval_min_score,
        semantic_weight=settings.retrieval_semantic_weight,
    )
    request.app.state.retrieval_service = service
    return service


def get_qa_service(
    retrieval: Annotated[RetrievalService, Depends(get_retrieval_service)],
    llm: Annotated[LLMProvider, Depends(get_llm_provider)],
) -> QAService:
    return QAService(retrieval, llm)
