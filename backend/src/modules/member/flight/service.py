"""航班搜索服务 - 使用 Document Store"""
from datetime import datetime

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import AirportInfo, FlightResponse


DOC_TYPE = "member_flight"


class FlightService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def search(
        self,
        departure_code: str,
        arrival_code: str,
        departure_date: str,
        cabin_class: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[FlightResponse]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        # 解析日期
        target_date = departure_date[:10]  # YYYY-MM-DD
        
        # 过滤
        filtered = []
        for doc in docs:
            data = doc["data"]
            if data.get("departure_code") != departure_code:
                continue
            if data.get("arrival_code") != arrival_code:
                continue
            # 检查日期
            dep_time = data.get("departure_time", "")
            if not dep_time.startswith(target_date):
                continue
            if cabin_class and data.get("cabin_class") != cabin_class:
                continue
            if min_price is not None and data.get("price", 0) < min_price:
                continue
            if max_price is not None and data.get("price", float("inf")) > max_price:
                continue
            filtered.append(self._to_response(doc))
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end]

    def find_by_id(self, id: str) -> FlightResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, f"Flight {id} not found")
        return self._to_response(doc)

    def _to_response(self, doc: dict) -> FlightResponse:
        data = doc["data"]
        return FlightResponse(
            id=doc["id"],
            airline=data.get("airline"),
            flight_number=data.get("flight_number"),
            departure=AirportInfo(
                code=data.get("departure_code"),
                name=data.get("departure_name"),
                city=data.get("departure_city"),
                time=data.get("departure_time"),
            ),
            arrival=AirportInfo(
                code=data.get("arrival_code"),
                name=data.get("arrival_name"),
                city=data.get("arrival_city"),
                time=data.get("arrival_time"),
            ),
            duration=data.get("duration"),
            stops=data.get("stops"),
            price=data.get("price"),
            currency=data.get("currency"),
            cabin_class=data.get("cabin_class"),
            available_seats=data.get("available_seats"),
        )
