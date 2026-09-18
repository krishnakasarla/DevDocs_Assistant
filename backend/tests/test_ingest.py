from scripts.ingest import build_chunks, sections, token_chunks


class FakeTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return list(range(len(text.split())))

    def decode(self, token_ids: list[int]) -> str:
        return " ".join(f"token-{token_id}" for token_id in token_ids)


class FakeModel:
    tokenizer = FakeTokenizer()


class LimitedFakeModel(FakeModel):
    max_seq_length = 8


def test_sections_preserve_heading_hierarchy():
    markdown = "## Parent\nintro\n### Child\ndetail"
    assert sections(markdown, "fallback") == [
        ("Parent", "intro"),
        ("Parent > Child", "detail"),
    ]


def test_build_chunks_is_stable(tmp_path):
    docs = tmp_path / "fastapi"
    docs.mkdir()
    (docs / "guide.md").write_text("## Setup\n" + "word " * 500, encoding="utf-8")

    first = build_chunks(tmp_path, FakeModel())
    second = build_chunks(tmp_path, FakeModel())

    assert len(first) == 3
    assert [chunk.content_hash for chunk in first] == [
        chunk.content_hash for chunk in second
    ]
    assert len({chunk.chunk_id for chunk in first}) == len(first)


def test_token_chunks_respect_embedding_model_limit():
    chunks = token_chunks("word " * 12, LimitedFakeModel())

    assert chunks
    assert all(len(chunk.split()) <= 6 for chunk in chunks)
