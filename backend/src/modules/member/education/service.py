"""教育搜索服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import EducationResponse


DOC_TYPE = "member_education"


class EducationService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def search(
        self,
        degree: str | None = None,
        major: str | None = None,
        city: str | None = None,
        max_tuition: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[EducationResponse]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        # 过滤
        filtered = []
        for doc in docs:
            data = doc["data"]
            if degree and data.get("degree") != degree:
                continue
            if major and data.get("major") != major:
                continue
            if city and data.get("city") != city:
                continue
            if max_tuition is not None and data.get("tuition", float("inf")) > max_tuition:
                continue
            filtered.append(self._to_response(doc))
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end]

    def find_by_id(self, id: str) -> EducationResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, f"Education {id} not found")
        return self._to_response(doc)

    def _to_response(self, doc: dict) -> EducationResponse:
        data = doc["data"]
        return EducationResponse(
            id=doc["id"],
            institution=data.get("institution"),
            program=data.get("program"),
            degree=data.get("degree"),
            major=data.get("major"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            tuition=data.get("tuition"),
            currency=data.get("currency"),
            duration=data.get("duration"),
            overall_ranking=data.get("overall_ranking"),
            program_ranking=data.get("program_ranking"),
            admission_rate=data.get("admission_rate"),
            employment_rate=data.get("employment_rate"),
        )
