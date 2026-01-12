"""房产搜索服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import HouseResponse


DOC_TYPE = "member_house"


class HouseService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def search(
        self,
        city: str | None = None,
        listing_type: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_bedrooms: int | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[HouseResponse]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        # 过滤
        filtered = []
        for doc in docs:
            data = doc["data"]
            if city and data.get("city") != city:
                continue
            if listing_type and data.get("listing_type") != listing_type:
                continue
            if min_price is not None and data.get("price", 0) < min_price:
                continue
            if max_price is not None and data.get("price", float("inf")) > max_price:
                continue
            if min_bedrooms is not None and data.get("bedrooms", 0) < min_bedrooms:
                continue
            filtered.append(self._to_response(doc))
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end]

    def find_by_id(self, id: str) -> HouseResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, f"House {id} not found")
        return self._to_response(doc)

    def _to_response(self, doc: dict) -> HouseResponse:
        data = doc["data"]
        return HouseResponse(
            id=doc["id"],
            listing_type=data.get("listing_type"),
            property_type=data.get("property_type"),
            city=data.get("city"),
            state=data.get("state"),
            price=data.get("price"),
            currency=data.get("currency"),
            bedrooms=data.get("bedrooms"),
            bathrooms=data.get("bathrooms"),
            square_feet=data.get("square_feet"),
            year_built=data.get("year_built"),
            features=data.get("features") or [],
        )
