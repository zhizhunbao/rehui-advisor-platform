"""酒店搜索服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import HotelResponse


DOC_TYPE = "member_hotel"


class HotelService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def search(
        self,
        city: str,
        min_price: float | None = None,
        max_price: float | None = None,
        min_rating: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[HotelResponse]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        # 过滤
        filtered = []
        for doc in docs:
            data = doc["data"]
            if data.get("city") != city:
                continue
            if min_price is not None and data.get("price_per_night", 0) < min_price:
                continue
            if max_price is not None and data.get("price_per_night", float("inf")) > max_price:
                continue
            if min_rating is not None and data.get("review_score", 0) < min_rating:
                continue
            filtered.append(self._to_response(doc))
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end]

    def find_by_id(self, id: str) -> HotelResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, f"Hotel {id} not found")
        return self._to_response(doc)

    def _to_response(self, doc: dict) -> HotelResponse:
        data = doc["data"]
        return HotelResponse(
            id=doc["id"],
            name=data.get("name"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            rating=data.get("rating"),
            review_score=data.get("review_score"),
            price_per_night=data.get("price_per_night"),
            currency=data.get("currency"),
            amenities=data.get("amenities") or [],
        )
