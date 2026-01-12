"""投资搜索服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import InvestmentResponse


DOC_TYPE = "member_investment"


class InvestmentService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def search(
        self,
        investment_type: str | None = None,
        risk_level: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[InvestmentResponse]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        # 过滤
        filtered = []
        for doc in docs:
            data = doc["data"]
            if investment_type and data.get("type") != investment_type:
                continue
            if risk_level and data.get("risk_level") != risk_level:
                continue
            if min_price is not None and data.get("current_price", 0) < min_price:
                continue
            if max_price is not None and data.get("current_price", float("inf")) > max_price:
                continue
            filtered.append(self._to_response(doc))
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end]

    def find_by_id(self, id: str) -> InvestmentResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, f"Investment {id} not found")
        return self._to_response(doc)

    def _to_response(self, doc: dict) -> InvestmentResponse:
        data = doc["data"]
        return InvestmentResponse(
            id=doc["id"],
            product_name=data.get("product_name"),
            type=data.get("type"),
            ticker=data.get("ticker"),
            current_price=data.get("current_price"),
            currency=data.get("currency"),
            risk_level=data.get("risk_level"),
            minimum_investment=data.get("minimum_investment"),
            provider=data.get("provider"),
            description=data.get("description"),
            sector=data.get("sector"),
            dividend_yield=data.get("dividend_yield"),
        )
