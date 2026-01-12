"""汽车搜索服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import CarResponse


DOC_TYPE = "member_car"


class CarService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def search(
        self,
        make: str | None = None,
        model: str | None = None,
        min_year: int | None = None,
        max_year: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        condition: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[CarResponse]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        # 过滤
        filtered = []
        for doc in docs:
            data = doc["data"]
            if make and data.get("make") != make:
                continue
            if model and data.get("model") != model:
                continue
            if min_year and data.get("year", 0) < min_year:
                continue
            if max_year and data.get("year", 9999) > max_year:
                continue
            if min_price is not None and data.get("price", 0) < min_price:
                continue
            if max_price is not None and data.get("price", float("inf")) > max_price:
                continue
            if condition and data.get("condition") != condition:
                continue
            filtered.append(self._to_response(doc))
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end]

    def find_by_id(self, id: str) -> CarResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, f"Car {id} not found")
        return self._to_response(doc)

    def _to_response(self, doc: dict) -> CarResponse:
        data = doc["data"]
        return CarResponse(
            id=doc["id"],
            make=data.get("make"),
            model=data.get("model"),
            year=data.get("year"),
            condition=data.get("condition"),
            mileage=data.get("mileage"),
            price=data.get("price"),
            currency=data.get("currency"),
            color=data.get("color"),
            transmission=data.get("transmission"),
            fuel_type=data.get("fuel_type"),
            features=data.get("features") or [],
        )
