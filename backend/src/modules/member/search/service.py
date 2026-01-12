"""统一搜索服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from .dto import SearchResponse, SearchResultItem, UnifiedSearchRequest


# 领域到文档类型的映射
DOMAIN_DOC_TYPES = {
    "car": "member_car",
    "house": "member_house",
    "job": "member_job",
    "education": "member_education",
    "investment": "member_investment",
    "flight": "member_flight",
    "hotel": "member_hotel",
}


class SearchService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def search(self, request: UnifiedSearchRequest) -> SearchResponse:
        doc_type = DOMAIN_DOC_TYPES.get(request.domain)
        if not doc_type:
            return SearchResponse(
                items=[],
                total=0,
                page=request.page,
                page_size=request.page_size,
            )
        
        docs = self.store.find(doc_type, status="active", limit=1000)
        
        # 简单的关键词搜索
        filtered = []
        if request.query:
            query_lower = request.query.lower()
            for doc in docs:
                data = doc["data"]
                # 搜索所有字符串字段
                for value in data.values():
                    if isinstance(value, str) and query_lower in value.lower():
                        filtered.append(doc)
                        break
        else:
            filtered = docs
        
        # 分页
        total = len(filtered)
        start = (request.page - 1) * request.page_size
        end = start + request.page_size
        page_docs = filtered[start:end]
        
        items = [
            SearchResultItem(
                id=doc["id"],
                domain=request.domain,
                title=self._get_title(doc),
                description=self._get_description(doc),
                data=doc["data"],
            )
            for doc in page_docs
        ]

        return SearchResponse(
            items=items,
            total=total,
            page=request.page,
            page_size=request.page_size,
        )

    def _get_title(self, doc: dict) -> str:
        """从文档中提取标题"""
        data = doc["data"]
        # 尝试常见的标题字段
        for field in ["title", "name", "product_name", "institution", "company"]:
            if data.get(field):
                return data[field]
        return "Untitled"

    def _get_description(self, doc: dict) -> str:
        """从文档中提取描述"""
        data = doc["data"]
        if data.get("description"):
            return data["description"]
        # 构建简单描述
        parts = []
        for field in ["city", "state", "type", "category"]:
            if data.get(field):
                parts.append(str(data[field]))
        return ", ".join(parts) if parts else ""
