from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DevDocs Assistant"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "devdocs_assistant"
    faiss_index_path: Path = Path("data/index/docs.faiss")
    faiss_metadata_path: Path = Path("data/index/docs.json")
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_device: str = "cpu"
    embedding_batch_size: int = Field(default=8, ge=1, le=128)
    embedding_max_tokens: int = Field(default=254, ge=1, le=4096)
    retrieval_top_k: int = Field(default=5, ge=1, le=20)
    retrieval_candidate_multiplier: int = Field(default=4, ge=1, le=10)
    retrieval_min_score: float = Field(default=0.5, ge=-1.0, le=1.0)
    retrieval_semantic_weight: float = Field(default=0.65, ge=0.0, le=1.0)

    llm_provider: Literal["groq", "ollama"] = "ollama"
    groq_api_key: str | None = None
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str = "llama-3.3-70b-versatile"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    llm_timeout_seconds: float = 60.0

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
