"""推荐服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from .dto import (
    RecommendationItem,
    RecommendationRequest,
    RecommendationResponse,
)


DOC_TYPE = "member_recommendation"


class RecommendationService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def get_recommendations(
        self, request: RecommendationRequest
    ) -> RecommendationResponse:
        docs = self.store.find(
            DOC_TYPE, 
            status="active", 
            owner_id=request.user_id,
            limit=1000
        )
        
        # 过滤 domain
        filtered = []
        for doc in docs:
            data = doc["data"]
            if data.get("domain") == request.domain:
                filtered.append(doc)
        
        # 按 ranking 排序
        filtered.sort(key=lambda d: d["data"].get("ranking", 0))
        
        # 限制数量
        filtered = filtered[:request.limit]
        
        items = [self._to_item(doc) for doc in filtered]

        return RecommendationResponse(
            items=items,
            total=len(items),
        )

    def _to_item(self, doc: dict) -> RecommendationItem:
        data = doc["data"]
        return RecommendationItem(
            id=doc["id"],
            domain=data.get("domain"),
            item_id=data.get("item_id"),
            match_score=data.get("match_score"),
            ranking=data.get("ranking"),
            pros=data.get("pros") or [],
            cons=data.get("cons") or [],
            reasoning=data.get("reasoning"),
        )
