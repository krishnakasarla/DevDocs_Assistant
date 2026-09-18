import pytest

from app.llm.base import LLMProvider
from app.services.qa_service import QAService


class FakeLLMProvider(LLMProvider):
    def __init__(self, response: str = "fake") -> None:
        self.called = False
        self.response = response

    async def generate(self, prompt: str, **kwargs) -> str:
        self.called = True
        return self.response


class EmptyRetrieval:
    async def search(self, query: str):
        return []


@pytest.mark.asyncio
async def test_empty_retrieval_does_not_call_llm():
    llm = FakeLLMProvider()
    service = QAService(EmptyRetrieval(), llm)  # type: ignore[arg-type]

    answer, sources = await service.answer("unknown")

    assert "don't know" in answer
    assert sources == []
    assert llm.called is False


class OneResultRetrieval:
    async def search(self, query: str):
        del query
        from app.models.schemas import SourceChunk

        return [
            SourceChunk(
                chunk_id="one",
                source_file="fastapi/tutorial/body.md",
                section_title="Request Body",
                doc_type="fastapi",
                chunk_text="Use a Pydantic model.",
                score=0.8,
            )
        ]


@pytest.mark.asyncio
async def test_model_insufficiency_keeps_natural_answer_but_removes_sources():
    llm = FakeLLMProvider(
        "CONTEXT_SUFFICIENT: no\nI don't have enough documentation to answer that."
    )
    service = QAService(OneResultRetrieval(), llm)  # type: ignore[arg-type]

    answer, sources = await service.answer("question")

    assert answer == "I don't have enough documentation to answer that."
    assert sources == []


@pytest.mark.asyncio
async def test_model_sufficiency_marker_is_removed_from_answer():
    llm = FakeLLMProvider("CONTEXT_SUFFICIENT: yes\nUse a Pydantic model.")
    service = QAService(OneResultRetrieval(), llm)  # type: ignore[arg-type]

    answer, sources = await service.answer("question")

    assert answer == "Use a Pydantic model."
    assert len(sources) == 1
