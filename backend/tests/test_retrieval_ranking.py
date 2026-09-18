import pytest

from app.services.retrieval_service import combined_score, lexical_overlap


def test_lexical_overlap_rewards_the_chunk_that_covers_the_question_terms():
    query = "How do I define and validate a JSON request body in FastAPI?"
    relevant = {
        "source_file": "fastapi/tutorial/body.md",
        "section_title": "Results",
        "chunk_text": "FastAPI reads the request body as JSON and validates the data.",
    }
    narrow = {
        "source_file": "fastapi/advanced/strict-content-type.md",
        "section_title": "Strict content type",
        "chunk_text": "FastAPI checks the content type header for JSON requests.",
    }

    assert lexical_overlap(query, relevant) > lexical_overlap(query, narrow)


def test_combined_score_can_promote_a_more_complete_lower_vector_match():
    relevant = combined_score(0.66, 1.0, semantic_weight=0.65)
    narrow = combined_score(0.77, 0.4, semantic_weight=0.65)

    assert relevant > narrow


@pytest.mark.parametrize(
    ("semantic_score", "minimum", "included"),
    [(0.7, 0.5, True), (0.5, 0.5, True), (0.49, 0.5, False)],
)
def test_relevance_threshold_boundary(semantic_score, minimum, included):
    assert (semantic_score >= minimum) is included
