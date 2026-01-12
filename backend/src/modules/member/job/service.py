"""工作搜索服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import JobResponse


DOC_TYPE = "member_job"


class JobService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def search(
        self,
        city: str | None = None,
        job_type: str | None = None,
        min_salary: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[JobResponse]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        # 过滤
        filtered = []
        for doc in docs:
            data = doc["data"]
            if city and data.get("city") != city:
                continue
            if job_type and data.get("job_type") != job_type:
                continue
            if min_salary is not None and data.get("salary_min", 0) < min_salary:
                continue
            filtered.append(self._to_response(doc))
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end]

    def find_by_id(self, id: str) -> JobResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, f"Job {id} not found")
        return self._to_response(doc)

    def _to_response(self, doc: dict) -> JobResponse:
        data = doc["data"]
        return JobResponse(
            id=doc["id"],
            title=data.get("title"),
            company=data.get("company"),
            city=data.get("city"),
            state=data.get("state"),
            job_type=data.get("job_type"),
            salary_min=data.get("salary_min"),
            salary_max=data.get("salary_max"),
            currency=data.get("currency"),
            description=data.get("description"),
            requirements=data.get("requirements") or [],
            benefits=data.get("benefits") or [],
        )
