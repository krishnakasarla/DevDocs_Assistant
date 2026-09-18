from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class QueryRequest(BaseModel):
    session_id: str | None = Field(default=None, min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=4000)

    @field_validator("question")
    @classmethod
    def question_must_have_content(cls, value: str) -> str:
        if not (cleaned := value.strip()):
            raise ValueError("question must not be blank")
        return cleaned


class SourceChunk(BaseModel):
    chunk_id: str
    source_file: str
    section_title: str
    doc_type: str
    chunk_text: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    session_id: str


class ChatMessage(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    timestamp: datetime
    sources: list[SourceChunk] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class PaginatedHistory(BaseModel):
    items: list[ChatMessage]
    page: int
    page_size: int
    total: int


class SessionSummary(BaseModel):
    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int


class SectionStat(BaseModel):
    source_file: str
    section_title: str
    count: int


class VolumePoint(BaseModel):
    date: str
    count: int


class StatsResponse(BaseModel):
    most_queried_sections: list[SectionStat]
    query_volume_over_time: list[VolumePoint]
    average_sources_per_answer: float
