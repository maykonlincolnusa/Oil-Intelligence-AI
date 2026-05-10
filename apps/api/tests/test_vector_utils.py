from app.services.vector_store_service import VectorStoreService


def test_cosine_similarity_handles_bad_vectors() -> None:
    assert VectorStoreService._cosine_similarity([], [1.0, 2.0]) == 0.0
    assert VectorStoreService._cosine_similarity([1.0], [1.0, 2.0]) == 0.0
