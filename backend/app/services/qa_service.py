from app.llm.base import LLMProvider
from app.models.schemas import SourceChunk
from app.services.retrieval_service import RetrievalService


class QAService:
    def __init__(self, retrieval: RetrievalService, llm: LLMProvider) -> None:
        self.retrieval = retrieval
        self.llm = llm

    async def answer(self, question: str) -> tuple[str, list[SourceChunk]]:
        sources = await self.retrieval.search(question)
        if not sources:
            return (
                "I don't know based on the indexed documentation. "
                "No relevant context was found.",
                [],
            )
        context = "\n\n".join(
            f"[Source {index}: {source.source_file} — {source.section_title}]\n"
            f"{source.chunk_text}"
            for index, source in enumerate(sources, start=1)
        )
        prompt = f"""You are DevDocs Assistant. Answer using only the context below.
Do not rely on outside knowledge. Cite every factual claim using the exact format
[source_file — section_title]. If the context is insufficient, say that you don't know.
Be concise and practical.

On the first line, output exactly CONTEXT_SUFFICIENT: yes when the supplied context
contains enough information to answer, or CONTEXT_SUFFICIENT: no when it does not.
Write the natural-language response on the following lines.

Context:
{context}

Question: {question}
Answer:"""
        answer = await self.llm.generate(prompt)
        first_line, separator, remainder = answer.partition("\n")
        marker = first_line.strip(" `").lower()
        if marker == "context_sufficient: no":
            return (remainder.strip() if separator else answer), []
        if marker == "context_sufficient: yes":
            return (remainder.strip() if separator else answer), sources
        return answer, sources
