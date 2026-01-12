from sqlalchemy.ext.asyncio import AsyncSession

from .dto import SearchResponse, SearchResultItem, UnifiedSearchRequest


class SearchService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def search(self, request: UnifiedSearchRequest) -> SearchResponse:
        # TODO: 实现统一搜索逻辑，根据 domain 调用对应的 service
        # 目前返回空结果
        return SearchResponse(
            items=[],
            total=0,
            page=request.page,
            page_size=request.page_size,
        )
