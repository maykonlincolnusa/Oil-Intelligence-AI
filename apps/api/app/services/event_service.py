from sqlalchemy.ext.asyncio import AsyncSession

from app.clients import GDELTClient
from app.core.config import get_settings
from app.models.event import GeopoliticalEvent
from app.repositories import EventRepository
from app.services.event_classifier import EventClassifierService
from app.services.llm import get_llm_provider


class EventService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        settings = get_settings()
        self.event_repo = EventRepository(session)
        llm_provider = get_llm_provider() if settings.openai_api_key else None
        self.classifier = EventClassifierService(llm_provider=llm_provider)
        self.gdelt_client = GDELTClient(api_key=settings.gdelt_api_key)

    async def get_events(self, limit: int = 100, offset: int = 0) -> list[GeopoliticalEvent]:
        events = await self.event_repo.get_events(limit=limit, offset=offset)
        if events:
            return events
        await self.ingest_mock_events()
        return await self.event_repo.get_events(limit=limit, offset=offset)

    async def count_events(self) -> int:
        return await self.event_repo.count_events()

    async def classify_event(self, headline: str, description: str) -> dict:
        result = await self.classifier.classify(headline=headline, description=description)
        return {
            "oil_impact": result.oil_impact,
            "sentiment": result.sentiment,
            "risk_level": result.risk_level,
            "categories": result.categories,
            "affected_assets": result.affected_assets,
            "affected_regions": result.affected_regions,
            "confidence_score": result.confidence_score,
            "reasoning": result.reasoning,
        }

    async def ingest_mock_events(self) -> None:
        payload = await self.gdelt_client.fetch_oil_news_events()
        for row in payload:
            classified = await self.classifier.classify(
                headline=row["headline"], description=row["description"]
            )
            self.session.add(
                GeopoliticalEvent(
                    event_time=row["event_time"],
                    headline=row["headline"],
                    description=row["description"],
                    oil_impact=classified.oil_impact,
                    sentiment=classified.sentiment,
                    risk_level=classified.risk_level,
                    categories=classified.categories,
                    affected_assets=classified.affected_assets,
                    affected_regions=classified.affected_regions,
                    confidence_score=classified.confidence_score,
                    source=row.get("source", "GDELT_MOCK"),
                    metadata_json={"ingestion": "mock"},
                )
            )
        await self.session.commit()
