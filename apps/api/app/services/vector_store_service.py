from math import sqrt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vector import EmbeddingDocument


class VectorStoreService:
    """pgvector-ready service with JSON embedding fallback.

    TODO: switch similarity search to native `<=>` operator once pgvector extension is installed.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_document(self, namespace: str, content: str, embedding: list[float], metadata: dict) -> None:
        self.session.add(
            EmbeddingDocument(
                namespace=namespace,
                content=content,
                embedding_json=embedding,
                metadata_json=metadata,
            )
        )
        await self.session.commit()

    async def search(self, namespace: str, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        rows = await self.session.execute(
            select(EmbeddingDocument).where(EmbeddingDocument.namespace == namespace)
        )
        docs = list(rows.scalars().all())

        scored = [
            (doc, self._cosine_similarity(query_embedding, doc.embedding_json or []))
            for doc in docs
        ]
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)[:top_k]
        return [
            {
                "id": doc.id,
                "content": doc.content,
                "score": score,
                "metadata": doc.metadata_json,
            }
            for doc, score in ranked
        ]

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b, strict=True))
        norm_a = sqrt(sum(x * x for x in a))
        norm_b = sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
