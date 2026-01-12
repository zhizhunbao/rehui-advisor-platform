from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.recommendation import Recommendation
from .dto import (
    RecommendationItem,
    RecommendationRequest,
    RecommendationResponse,
)


class RecommendationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_recommendations(
        self, request: RecommendationRequest
    ) -> RecommendationResponse:
        query = (
            select(Recommendation)
            .where(Recommendation.user_id == request.user_id)
            .where(Recommendation.domain == request.domain)
            .order_by(Recommendation.ranking)
            .limit(request.limit)
        )

        result = await self.db.execute(query)
        items = list(result.scalars().all())

        return RecommendationResponse(
            items=[self._to_item(r) for r in items],
            total=len(items),
        )

    def _to_item(self, rec: Recommendation) -> RecommendationItem:
        return RecommendationItem(
            id=rec.id,
            domain=rec.domain,
            item_id=rec.item_id,
            match_score=rec.match_score,
            ranking=rec.ranking,
            pros=rec.pros or [],
            cons=rec.cons or [],
            reasoning=rec.reasoning,
        )
